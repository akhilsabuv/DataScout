import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, delay, tap } from 'rxjs';

export interface Column {
    name: string;
    type: string;
    description: string;
    isLocked: boolean;
}

export interface Table {
    name: string;
    context?: string; // Table-level description/prompt
    columns?: Column[]; // Optional, loaded on expand
    isExpanded?: boolean; // UI state
}

@Injectable({
    providedIn: 'root'
})
export class DbSchemaService {

    private apiUrl = 'http://127.0.0.1:8000';

    // Mock Data (kept for fallback/testing if needed, but primary is now API)
    private mockTables: Table[] = [];
    private mockColumns: { [key: string]: Column[] } = {};

    // State
    private currentTables: Table[] = [];
    private currentDbType: string = '';
    private currentDbName: string = '';
    private currentConnectionId: number | null = null;

    constructor(private http: HttpClient) { }

    setSchemaData(tables: any[], dbType: string, dbName: string, connectionId: number) {
        this.currentDbType = dbType;
        this.currentDbName = dbName;
        this.currentConnectionId = connectionId;

        // Transform API response to Table interface
        this.currentTables = tables.map(t => ({
            name: t.name,
            context: t.table_context || '', // Load context if available (needs backend to return it, currently backend returns schema list, we might need to fetch saved schema details or assume they are in the list if we updated the return model)
            // Actually, the backend returns the schema from the DB engine, which doesn't have our context.
            // We need to fetch the saved context/descriptions from our internal DB.
            // BUT, for now, let's assume the backend "save" returns the ID, and we might need to re-fetch the "saved" schema to get the contexts?
            // Or, the backend `save_connection_details` saves it.
            // Wait, the requirement is "load the data in schema from the database".
            // So when we connect, we should probably fetch the *saved* schema if it exists, or merge it.
            // For now, let's just implement the SAVE part as requested "data from the schema page should also be saved in db".
            // Loading part: "load the data in schema from the database".
            // This implies when we connect, if we have saved data, we should load it.
            // The current backend implementation of `connect_*` fetches fresh schema from the target DB and saves it to internal DB.
            // It does NOT return the saved context/descriptions yet.
            // I need to update the backend to return the saved info if available.
            // But let's finish the frontend service update first to handle the saving.
            columns: t.columns.map((c: any) => ({
                name: c.name,
                type: c.type,
                description: '', // Placeholder, see above note
                isLocked: false
            }))
        }));
    }

    getDbType(): string {
        return this.currentDbType;
    }

    getDbName(): string {
        return this.currentDbName;
    }

    getTables(): Observable<Table[]> {
        return of(this.currentTables);
    }

    getColumns(tableName: string): Observable<Column[]> {
        const table = this.currentTables.find(t => t.name === tableName);
        if (table && table.columns) {
            return of(table.columns);
        }
        return of([]);
    }

    // API: Save column description
    saveDescription(tableName: string, columnName: string, description: string): Observable<any> {
        if (!this.currentConnectionId) return of(null);
        return this.http.put(`${this.apiUrl}/schema/${this.currentConnectionId}/column/${tableName}/${columnName}/description`, { description });
    }

    // API: Save table context
    saveTableContext(tableName: string, context: string): Observable<any> {
        if (!this.currentConnectionId) return of(null);
        return this.http.put(`${this.apiUrl}/schema/${this.currentConnectionId}/table/${tableName}/context`, { context });
    }

    // API: Save global schema context
    saveGlobalContext(context: string): Observable<any> {
        if (!this.currentConnectionId) return of(null);
        return this.http.put(`${this.apiUrl}/schema/${this.currentConnectionId}/global/context`, { context });
    }

    // API: Toggle lock state
    toggleLock(tableName: string, columnName: string, isLocked: boolean): Observable<boolean> {
        console.log(`Toggling lock for ${tableName}.${columnName} to ${isLocked}`);
        return of(true);
    }

    // API: Delete connection (reset DB)
    deleteConnection(): Observable<any> {
        return this.http.delete(`${this.apiUrl}/connection`).pipe(
            tap(() => {
                this.currentTables = [];
                this.currentDbType = '';
                this.currentDbName = '';
                this.currentConnectionId = null;
            })
        );
    }
}
