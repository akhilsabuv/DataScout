import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';
import { DbSchemaService } from '../services/db-schema.service';
import { ToastService } from '../shared/toast/toast.service';
import { ConfirmationModalService } from '../shared/confirmation-modal/confirmation-modal.service';

@Component({
  selector: 'app-db-connection',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './db-connection.component.html',
  styleUrl: './db-connection.component.css'
})
export class DbConnectionComponent {
  selectedDb: string = 'sqlite';

  // SQLite
  sqliteFile: any = null;

  // MSSQL / PostgreSQL / MySQL
  host: string = '';
  port: string = '';
  dbName: string = '';
  username: string = '';
  password: string = '';
  showPassword: boolean = false;

  isLoading: boolean = false;

  constructor(
    private router: Router,
    private apiService: ApiService,
    private schemaService: DbSchemaService,
    private toastService: ToastService,
    private modalService: ConfirmationModalService
  ) { }

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.sqliteFile = file;
      console.log('Selected file:', file.name);
    }
  }

  getPortPlaceholder(): string {
    switch (this.selectedDb) {
      case 'mssql': return '1433';
      case 'postgresql': return '5432';
      case 'mysql': return '3306';
      default: return 'Port';
    }
  }

  onConnect() {
    if (this.isLoading) return;

    console.log('Connecting to:', this.selectedDb);
    this.isLoading = true;

    let observable;
    let dbNameForDisplay = this.dbName;

    if (this.selectedDb === 'sqlite') {
      observable = this.apiService.connectSQLite({ path: this.sqliteFile ? this.sqliteFile.name : '' });
      dbNameForDisplay = this.sqliteFile ? this.sqliteFile.name : 'Unknown DB';
    } else if (this.selectedDb === 'mysql') {
      observable = this.apiService.connectMySQL({
        host: this.host,
        port: parseInt(this.port) || 3306,
        database: this.dbName,
        username: this.username,
        password: this.password
      });
    } else if (this.selectedDb === 'mssql') {
      observable = this.apiService.connectMSSQL({
        host: this.host,
        port: parseInt(this.port) || 1433,
        database: this.dbName,
        username: this.username,
        password: this.password
      });
    } else if (this.selectedDb === 'postgresql') {
      observable = this.apiService.connectPostgreSQL({
        host: this.host,
        port: parseInt(this.port) || 5432,
        database: this.dbName,
        username: this.username,
        password: this.password
      });
    }

    if (observable) {
      observable.subscribe({
        next: (response) => {
          console.log('Connection successful', response);
          this.schemaService.setSchemaData(response.tables, this.selectedDb, dbNameForDisplay, response.connection_id);
          this.router.navigate(['/schema']);
          this.isLoading = false;
        },
        error: (error) => {
          console.error('Connection failed', error);
          this.modalService.confirm({
            title: 'Connection Failed',
            message: error.error?.detail || error.message || 'An unknown error occurred while connecting to the database.',
            confirmText: 'OK',
            cancelText: 'Close', // Optional, but good to have
            type: 'danger'
          });
          this.isLoading = false;
        }
      });
    } else {
      this.isLoading = false;
    }
  }
}
