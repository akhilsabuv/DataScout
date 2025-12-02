import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface ChatMessage {
  role: 'user' | 'agent';
  content: string;
  timestamp: Date;
  type?: 'text' | 'table';
  data?: any;
}

interface SqlQuery {
  query: string;
  timestamp: Date;
  status: 'success' | 'error' | 'blocked';
}

@Component({
  selector: 'app-agent-interface',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './agent-interface.component.html',
  styleUrl: './agent-interface.component.css'
})
export class AgentInterfaceComponent {
  messages: ChatMessage[] = [
    {
      role: 'agent',
      content: 'Hello! I am your business intelligence assistant. You can ask me anything about your business data.',
      timestamp: new Date()
    }
  ];

  sqlHistory: SqlQuery[] = [
    {
      query: 'SELECT * FROM users LIMIT 5;',
      timestamp: new Date(Date.now() - 100000),
      status: 'success'
    },
    {
      query: 'SELECT COUNT(*) FROM orders WHERE status = "pending";',
      timestamp: new Date(Date.now() - 50000),
      status: 'success'
    },
    {
      query: 'DROP TABLE users;',
      timestamp: new Date(Date.now() - 20000),
      status: 'blocked'
    }
  ];

  userInput: string = '';

  sendMessage() {
    if (!this.userInput.trim()) return;

    // Add user message
    this.messages.push({
      role: 'user',
      content: this.userInput,
      timestamp: new Date()
    });

    const currentInput = this.userInput;
    this.userInput = '';

    // Simulate agent response and SQL generation
    setTimeout(() => {
      const mockSql = `SELECT * FROM data WHERE keyword LIKE '%${currentInput}%'`;

      this.sqlHistory.unshift({
        query: mockSql,
        timestamp: new Date(),
        status: 'success'
      });

      this.messages.push({
        role: 'agent',
        content: `I've generated a query to find data related to "${currentInput}". Here are the results...`,
        timestamp: new Date()
      });
    }, 1000);

    // Simulate a table response for specific keywords
    if (this.userInput.toLowerCase().includes('report') || this.userInput.toLowerCase().includes('table')) {
      setTimeout(() => {
        this.messages.push({
          role: 'agent',
          content: 'Here is the data you requested:',
          timestamp: new Date(),
          type: 'table',
          data: {
            columns: ['ID', 'Name', 'Role', 'Status'],
            rows: [
              [101, 'Alice Johnson', 'Admin', 'Active'],
              [102, 'Bob Smith', 'User', 'Inactive'],
              [103, 'Charlie Brown', 'Editor', 'Active'],
              [104, 'Diana Prince', 'User', 'Pending']
            ]
          }
        });
      }, 1500);
    }
  }
}
