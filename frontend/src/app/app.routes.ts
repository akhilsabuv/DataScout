import { Routes } from '@angular/router';
import { DbConnectionComponent } from './db-connection/db-connection.component';
import { DbSchemaViewerComponent } from './db-schema-viewer/db-schema-viewer.component';
import { AgentInterfaceComponent } from './agent-interface/agent-interface.component';

export const routes: Routes = [
    { path: '', redirectTo: '/connect', pathMatch: 'full' },
    { path: 'connect', component: DbConnectionComponent },
    { path: 'schema', component: DbSchemaViewerComponent },
    { path: 'agent', component: AgentInterfaceComponent }
];
