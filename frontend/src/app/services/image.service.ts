import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Observable } from 'rxjs/Observable';
import { environment } from '../../environments/environment';
@Injectable()
export class ImageService {

    constructor(private apiService: ApiService) { }

    // if isUpload, then call Upload API
    compare(file: File, isUpload: boolean = false): Promise<any> {
        return new Promise((resolve, reject) => {

            const xhr: XMLHttpRequest = new XMLHttpRequest();
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        // alert(xhr.response);
                        try {
                            const json = JSON.parse(xhr.response);
                            resolve(json);
                        } catch {
                            resolve(xhr.response);
                        }
                    } else {
                        reject(xhr.response);
                    }
                }
            };
            const url = isUpload ? `${environment.API_URL}task/upload` : `${environment.API_URL}task/compare`;
            xhr.open('POST', url, true);

            const formData = new FormData();
            formData.append('image', file, file.name);
            xhr.send(formData);
        });
    }
    upload(image) {
        return this.apiService.post_file('task/upload', {});
    }
}
