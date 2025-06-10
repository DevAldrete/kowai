import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

@Injectable({
  providedIn: 'root',
})
export class WebSocketService {
  private socket$: WebSocketSubject<any>;

  constructor() {
    this.socket$ = webSocket('ws://localhost:8080/ws');
  }

  public connect() {
    return this.socket$.asObservable();
  }

  public sendMessage(message: any) {
    this.socket$.next(message);
  }

  public close() {
    this.socket$.complete();
  }
} 