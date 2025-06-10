import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';
import { WebSocketService } from '../services/websocket.service';
import { MarkdownModule } from 'ngx-markdown';
import { ConfigService, AppConfig } from '../services/config.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, MarkdownModule],
  template: `
    <div class="flex flex-col h-screen bg-kowai-background text-kowai-text">
      <div class="p-4 bg-kowai-primary text-kowai-text text-center">
        <h1 class="text-xl font-bold">KowAI Chat</h1>
        <p *ngIf="config">Using model: {{ config.model }}</p>
      </div>
      <div class="flex-grow p-4 overflow-auto">
        <div *ngFor="let message of messages" class="mb-2">
          <strong>{{ message.role }}:</strong>
          <markdown [data]="message.content"></markdown>
        </div>
      </div>
      <div class="p-4 bg-kowai-background">
        <form (ngSubmit)="sendMessage()" class="flex">
          <input
            type="text"
            [(ngModel)]="newMessage"
            name="newMessage"
            class="flex-grow p-2 rounded-l-lg bg-kowai-primary text-kowai-text focus:outline-none"
            placeholder="Type your message..."
          />
          <button
            type="submit"
            class="bg-kowai-primary text-kowai-text font-bold py-2 px-4 rounded-r-lg hover:bg-opacity-80 transition-colors"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  `,
})
export class ChatPageComponent implements OnInit, OnDestroy {
  messages: { role: string; content: string }[] = [];
  newMessage = '';
  config: AppConfig | null = null;
  private subscription: Subscription = new Subscription();

  constructor(
    private webSocketService: WebSocketService,
    private configService: ConfigService
  ) {}

  ngOnInit() {
    this.loadMessages();
    this.subscription.add(
      this.configService.getConfig().subscribe((config) => {
        this.config = config;
      })
    );
    this.subscription.add(
      this.webSocketService.connect().subscribe((message: any) => {
        if (message.type === 'stream') {
          const lastMessage = this.messages[this.messages.length - 1];
          if (lastMessage && lastMessage.role === 'assistant') {
            lastMessage.content += message.payload;
          } else {
            this.messages.push({ role: 'assistant', content: message.payload });
          }
          this.saveMessages();
        }
      })
    );
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  sendMessage() {
    if (this.newMessage.trim()) {
      const userMessage = { role: 'user', content: this.newMessage };
      this.messages.push(userMessage);
      this.saveMessages();
      this.webSocketService.sendMessage({
        type: 'chat',
        payload: this.newMessage,
      });
      this.newMessage = '';
    }
  }

  private saveMessages() {
    localStorage.setItem('chat_messages', JSON.stringify(this.messages));
  }

  private loadMessages() {
    const savedMessages = localStorage.getItem('chat_messages');
    if (savedMessages) {
      this.messages = JSON.parse(savedMessages);
    }
  }
} 