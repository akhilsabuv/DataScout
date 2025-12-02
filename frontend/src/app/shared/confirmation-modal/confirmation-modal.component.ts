import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConfirmationModalService, ModalConfig } from './confirmation-modal.service';
import { animate, style, transition, trigger } from '@angular/animations';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-confirmation-modal',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="modal-overlay" *ngIf="config" [@fadeInOut]>
      <div class="modal-container" [@scaleInOut] role="dialog" aria-modal="true">
        <div class="modal-header">
          <div class="icon-wrapper" [ngClass]="config.type || 'info'">
            <i class="bi" [ngClass]="getIcon(config.type)"></i>
          </div>
          <h3 class="modal-title">
            {{ config.title }}
          </h3>
        </div>
        
        <div class="modal-body">
          <p>{{ config.message }}</p>
        </div>

        <div class="modal-footer">
          <button class="btn btn-lg btn-secondary" (click)="cancel()">
            {{ config.cancelText || 'Cancel' }}
          </button>
          <button class="btn btn-lg" 
                  [ngClass]="getBtnClass(config.type)" 
                  (click)="confirm()">
            {{ config.confirmText || 'Confirm' }}
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.85); /* Darker backdrop */
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(4px);
    }

    .modal-container {
      background: #ffffff;
      border-radius: 16px;
      width: 95%;
      max-width: 520px;
      box-shadow: 0 0 0 100vmax rgba(0,0,0,0.5), 0 25px 50px -12px rgba(0, 0, 0, 0.5); /* Extreme shadow */
      overflow: hidden;
      display: flex;
      flex-direction: column;
      border: 2px solid #000000; /* Solid black border */
    }

    .modal-header {
      padding: 32px 32px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 16px;
      background: #ffffff;
      border-bottom: 1px solid #e5e7eb;
    }

    .icon-wrapper {
      width: 72px;
      height: 72px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 36px;
      margin-bottom: 4px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      border: 2px solid rgba(0,0,0,0.1);
    }

    .icon-wrapper.danger { background: #fee2e2; color: #dc2626; }
    .icon-wrapper.warning { background: #fef3c7; color: #d97706; }
    .icon-wrapper.info { background: #dbeafe; color: #2563eb; }

    .modal-title {
      margin: 0;
      font-size: 1.75rem;
      font-weight: 900; /* Extra bold */
      color: #000000; /* Pure black */
      line-height: 1.2;
    }

    .modal-body {
      padding: 24px 40px 32px;
      color: #000000; /* Pure black */
      line-height: 1.6;
      text-align: center;
      font-size: 1.2rem; /* Larger font */
      font-weight: 600; /* Bolder */
      background: #ffffff;
    }

    .modal-footer {
      padding: 24px 32px;
      background: #f3f4f6;
      display: flex;
      justify-content: stretch;
      gap: 16px;
      border-top: 2px solid #e5e7eb;
    }

    .modal-footer .btn {
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .btn {
      padding: 16px 24px;
      border-radius: 8px;
      font-weight: 800; /* Extra bold */
      cursor: pointer;
      border: 2px solid transparent;
      transition: all 0.2s ease;
      font-size: 1.1rem;
      letter-spacing: 0.02em;
      text-transform: uppercase;
    }

    .btn-secondary {
      background: #ffffff;
      border: 2px solid #000000; /* Solid black border */
      color: #000000;
    }
    .btn-secondary:hover { 
      background: #e5e7eb; 
      color: #000000;
    }

    .btn-danger { 
      background: #dc2626; 
      color: #ffffff; 
      border: 2px solid #991b1b;
      box-shadow: 0 4px 6px rgba(220, 38, 38, 0.4);
    }
    .btn-danger:hover { 
      background: #b91c1c; 
      transform: translateY(-2px); 
      box-shadow: 0 6px 8px rgba(220, 38, 38, 0.5); 
    }

    .btn-warning { 
      background: #d97706; 
      color: #ffffff; 
      border: 2px solid #92400e;
    }
    .btn-warning:hover { 
      background: #b45309; 
    }

    .btn-primary { 
      background: #2563eb; 
      color: #ffffff; 
      border: 2px solid #1e40af;
    }
    .btn-primary:hover { 
      background: #1d4ed8; 
    }
  `],
  animations: [
    trigger('fadeInOut', [
      transition(':enter', [
        style({ opacity: 0 }),
        animate('200ms ease-out', style({ opacity: 1 }))
      ]),
      transition(':leave', [
        animate('150ms ease-in', style({ opacity: 0 }))
      ])
    ]),
    trigger('scaleInOut', [
      transition(':enter', [
        style({ transform: 'scale(0.95)', opacity: 0 }),
        animate('200ms ease-out', style({ transform: 'scale(1)', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('150ms ease-in', style({ transform: 'scale(0.95)', opacity: 0 }))
      ])
    ])
  ]
})
export class ConfirmationModalComponent implements OnInit, OnDestroy {
  config: ModalConfig | null = null;
  private subscription: Subscription | null = null;

  constructor(
    public modalService: ConfirmationModalService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.subscription = this.modalService.modalState$.subscribe(config => {
      console.log('Modal State Updated:', config);
      this.config = config;
      this.cdr.detectChanges(); // Force update
    });
  }

  ngOnDestroy() {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }

  confirm() {
    this.modalService.resolve(true);
  }

  cancel() {
    this.modalService.resolve(false);
  }

  getIcon(type?: string): string {
    switch (type) {
      case 'danger': return 'bi-exclamation-octagon-fill';
      case 'warning': return 'bi-exclamation-triangle-fill';
      default: return 'bi-info-circle-fill';
    }
  }

  getBtnClass(type?: string): string {
    switch (type) {
      case 'danger': return 'btn-danger';
      case 'warning': return 'btn-warning';
      default: return 'btn-primary';
    }
  }
}
