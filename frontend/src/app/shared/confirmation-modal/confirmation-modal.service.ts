import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';

export interface ModalConfig {
    title: string;
    message: string;
    confirmText?: string;
    cancelText?: string;
    type?: 'danger' | 'warning' | 'info';
}

@Injectable({
    providedIn: 'root'
})
export class ConfirmationModalService {
    private modalStateSubject = new BehaviorSubject<ModalConfig | null>(null);
    modalState$ = this.modalStateSubject.asObservable();

    private confirmSubject = new Subject<boolean>();

    confirm(config: ModalConfig): Promise<boolean> {
        this.modalStateSubject.next(config);
        return new Promise((resolve) => {
            const sub = this.confirmSubject.subscribe((result) => {
                resolve(result);
                sub.unsubscribe();
                this.modalStateSubject.next(null); // Close modal
            });
        });
    }

    resolve(result: boolean) {
        this.confirmSubject.next(result);
    }
}
