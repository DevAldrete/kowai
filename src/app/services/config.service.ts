import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface AppConfig {
  model: string;
  version: string;
}

@Injectable({
  providedIn: 'root',
})
export class ConfigService {
  private configUrl = '/api/config';

  constructor(private http: HttpClient) {}

  getConfig(): Observable<AppConfig> {
    return this.http.get<AppConfig>(this.configUrl);
  }
} 