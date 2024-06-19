import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component, output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { RouterOutlet } from '@angular/router';
import { SocketIoModule, SocketIoConfig, Socket } from 'ngx-socket-io';
const config: SocketIoConfig = { url: 'http://localhost:5000', options: {} }
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,FormsModule,CommonModule, HttpClientModule,
    MatProgressBarModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'encoder';
  command: string = '';
  output: string = '';
  input_file:string=''
  output_file:string=''
  show_bar=false
  selectedFile: File | '' = '';
  progress: number | string = 0;
  constructor(private http: HttpClient) {
   
  


  }
  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }
  executeCommand(): void {
    this.output=''
    const formData = new FormData();
    formData.append('file', this.selectedFile);
    let request={
      'input_file':this.input_file
    }
    this.show_bar=true
   
    this.http.post<any>('http://127.0.0.1:5000/api/execute', 
     request)
      .subscribe(
        response => {
          this.output = response['result'];
          this.show_bar=false
        },
        error => {
          console.error('Error:', error);
          this.output = 'Error in Encoding';
          this.show_bar=false
          
        }
      );
  }

}
