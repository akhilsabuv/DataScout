import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { DbSchemaService, Table, Column } from '../services/db-schema.service';
import { ToastService } from '../shared/toast/toast.service';
import { ConfirmationModalService } from '../shared/confirmation-modal/confirmation-modal.service';

/*
  README:
  This component is designed to be plug-and-play with a real backend.
  
  Integration Steps:
  1. Update `DbSchemaService` to make real HTTP calls instead of returning mock data.
  2. Ensure the backend API matches the expected response format (Table[], Column[]).
  3. No changes should be needed in this component logic if the service interface remains consistent.
*/

@Component({
    selector: 'app-db-schema-viewer',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './db-schema-viewer.component.html',
    styleUrls: ['./db-schema-viewer.component.css']
})
export class DbSchemaViewerComponent implements OnInit {
    tables: Table[] = [];
    loadingTables: boolean = true;
    dbType: string = '';
    dbName: string = '';

    // Cache for columns to avoid refetching
    columnsCache: { [tableName: string]: Column[] } = {};
    loadingColumns: { [tableName: string]: boolean } = {};

    // UI States for saving
    savingStates: { [key: string]: 'idle' | 'saving' | 'saved' | 'error' } = {};

    constructor(
        private schemaService: DbSchemaService,
        private router: Router,
        private toastService: ToastService,
        private modalService: ConfirmationModalService
    ) { }

    ngOnInit() {
        this.dbType = this.schemaService.getDbType();
        this.dbName = this.schemaService.getDbName();

        if (!this.dbType || !this.dbName) {
            this.router.navigate(['/connect']);
            return;
        }

        this.loadTables();
    }

    loadTables() {
        this.loadingTables = true;
        this.schemaService.getTables().subscribe({
            next: (data) => {
                this.tables = data.map(t => ({ ...t, isExpanded: false }));
                this.loadingTables = false;
            },
            error: (err) => {
                console.error('Failed to load tables', err);
                this.toastService.error('Failed to load tables');
                this.loadingTables = false;
            }
        });
    }

    toggleTable(table: Table) {
        table.isExpanded = !table.isExpanded;

        if (table.isExpanded && !this.columnsCache[table.name]) {
            this.loadColumns(table);
        }
    }

    loadColumns(table: Table) {
        this.loadingColumns[table.name] = true;
        this.schemaService.getColumns(table.name).subscribe({
            next: (cols) => {
                this.columnsCache[table.name] = cols;
                this.loadingColumns[table.name] = false;
            },
            error: (err) => {
                console.error(`Failed to load columns for ${table.name}`, err);
                this.toastService.error(`Failed to load columns for ${table.name}`);
                this.loadingColumns[table.name] = false;
            }
        });
    }

    saveDescription(table: Table, col: Column) {
        if (col.isLocked) return;

        const key = `${table.name}-${col.name}`;
        this.savingStates[key] = 'saving';

        this.schemaService.saveDescription(table.name, col.name, col.description).subscribe({
            next: () => {
                this.savingStates[key] = 'saved';
                setTimeout(() => {
                    this.savingStates[key] = 'idle';
                }, 2000);
            },
            error: () => {
                this.savingStates[key] = 'error';
                this.toastService.error('Failed to save description');
            }
        });
    }

    saveTableContext(table: Table) {
        const key = `table-${table.name}`;
        this.savingStates[key] = 'saving';

        this.schemaService.saveTableContext(table.name, table.context || '').subscribe({
            next: () => {
                this.savingStates[key] = 'saved';
                setTimeout(() => {
                    this.savingStates[key] = 'idle';
                }, 2000);
            },
            error: () => {
                this.savingStates[key] = 'error';
                this.toastService.error('Failed to save table context');
            }
        });
    }

    toggleLock(table: Table, col: Column) {
        // Optimistic UI update
        col.isLocked = !col.isLocked;

        this.schemaService.toggleLock(table.name, col.name, col.isLocked).subscribe({
            error: () => {
                // Revert on error
                col.isLocked = !col.isLocked;
                console.error('Failed to toggle lock');
                this.toastService.error('Failed to toggle lock');
            }
        });
    }

    getSaveState(table: Table, col: Column): string {
        return this.savingStates[`${table.name}-${col.name}`] || 'idle';
    }

    getTableSaveState(table: Table): string {
        return this.savingStates[`table-${table.name}`] || 'idle';
    }

    // Global Context
    globalContext: string = '';
    globalContextSaveState: string = 'idle';

    saveGlobalContext() {
        this.globalContextSaveState = 'saving';
        this.schemaService.saveGlobalContext(this.globalContext).subscribe({
            next: () => {
                this.globalContextSaveState = 'saved';
                setTimeout(() => {
                    this.globalContextSaveState = 'idle';
                }, 2000);
            },
            error: () => {
                this.globalContextSaveState = 'error';
                this.toastService.error('Failed to save global context');
            }
        });
    }

    async connectToAgent() {
        const confirmed = await this.modalService.confirm({
            title: 'Connect to Agent',
            message: 'Are you sure you want to connect to the agent? This will initiate a secure session.',
            confirmText: 'Connect',
            type: 'info'
        });

        if (confirmed) {
            console.log('Connecting to agent...');
            // Placeholder for navigation to chat interface
            // this.router.navigate(['/chat']);
            this.toastService.info('Connecting to agent...');
        }
    }

    async deleteConnection() {
        const confirmed = await this.modalService.confirm({
            title: 'Delete Connection',
            message: 'Are you sure you want to delete this connection? This will reset the database and clear all saved context.',
            confirmText: 'Delete',
            type: 'danger'
        });

        if (confirmed) {
            this.schemaService.deleteConnection().subscribe({
                next: () => {
                    this.toastService.success('Connection deleted successfully');
                    this.router.navigate(['/connect']);
                },
                error: (err) => {
                    console.error('Failed to delete connection', err);
                    this.toastService.error('Failed to delete connection');
                }
            });
        }
    }
}
