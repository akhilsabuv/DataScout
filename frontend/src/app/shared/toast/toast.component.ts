import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToastService, Toast } from './toast.service';
import { animate, style, transition, trigger } from '@angular/animations';

@Component({
    selector: 'app-toast',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="toast-container">
      <div *ngFor="let toast of toastService.toasts$ | async" 
           class="toast-item" 
           [ngClass]="toast.type"
           [@flyInOut]>
        <div class="toast-content">
          <i class="bi" [ngClass]="getIcon(toast.type)"></i>
          <span>{{ toast.message }}</span>
        </div>
        <button class="close-btn" (click)="toastService.remove(toast.id)">
          <i class="bi bi-x"></i>
        </button>
      </div>
    </div>
  `,
    styles: [`
    .toast-container {
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .toast-item {
      min-width: 300px;
      padding: 12px 16px;
      border-radius: 8px;
      background: white;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #333;
      border-left: 4px solid transparent;
    }

    .toast-content {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 14px;
      font-weight: 500;
    }

    .close-btn {
      background: none;
      border: none;
      cursor: pointer;
      color: #999;
      padding: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }

    .close-btn:hover {
      color: #333;
    }

    /* Types */
    .success { border-left-color: #10b981; }
    .success i { color: #10b981; }

    .error { border-left-color: #ef4444; }
    .error i { color: #ef4444; }

    .info { border-left-color: #3b82f6; }
    .info i { color: #3b82f6; }

    .warning { border-left-color: #f59e0b; }
    .warning i { color: #f59e0b; }
  `],
    animations: [
        trigger('flyInOut', [
            transition(':enter', [
                style({ transform: 'translateX(100%)', opacity: 0 }),
                animate('300ms ease-out', style({ transform: 'translateX(0)', opacity: 1 }))
            ]),
            transition(':leave', [
                animate('200ms ease-in', style({ transform: 'translateX(100%)', opacity: 0 }))
            ])
        ])
    ]
})
export class ToastComponent {
    constructor(public toastService: ToastService) { }

    getIcon(type: string): string {
        switch (type) {
            case 'success': return 'bi-check-circle-fill';
            case 'error': return 'bi-exclamation-circle-fill';
            case 'warning': return 'bi-exclamation-triangle-fill';
            case 'info': return 'bi-info-circle-fill';
            default: return 'bi-info-circle';
        }
    }
}
