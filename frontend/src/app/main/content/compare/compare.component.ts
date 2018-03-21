import { Component, ViewChild, ElementRef } from '@angular/core';
import { Observable } from 'rxjs/Rx';
import { FuseTranslationLoaderService } from '../../../core/services/translation-loader.service';
import { ImageService } from '../../../services';
import { locale as english } from './i18n/en';
import { locale as turkish } from './i18n/tr';
import { Http } from '@angular/http';
import { RequestOptions } from '@angular/http';
declare let $: any;
@Component({
    selector: 'fuse-sample',
    templateUrl: './compare.component.html',
    styleUrls: ['./compare.component.scss']
})
export class CompareComponent {
    isLoading = false;
    isEnable = false;
    isResult = false;
    file: any;
    result = [];
    msgs = [];
    message: any;
    constructor(
        private translationLoader: FuseTranslationLoaderService,
        private imageService: ImageService,
        private http: Http) {
        this.translationLoader.loadTranslations(english, turkish);
    }
    onTapCompare() {
        this.isLoading = true;
        this.imageService.compare(this.file)
            .then(res => {
                this.isLoading = false;
                this.isResult = true;
                console.log(res);
                if (res.success) {
                    // this.dialog.open(DialogComponent);
                    this.message = 'Successfully uploaded';
                    this.msgs.push({ severity: 'success', summary: 'Success', detail: 'Successfully uploaded' });
                    setTimeout(() => { this.msgs = []; this.message = null; }, 2000);

                } else {
                    // this.dialog.open(DialogComponent);
                    this.message = res.message;
                    this.msgs.push({ severity: 'error', summary: 'Error', detail: res.message });
                    setTimeout(() => { this.msgs = []; this.message = null; }, 2000);
                }
                this.result = res;
            })
            .catch(error => {
                this.isLoading = false;
                console.error(error);
                this.message = error.message;
                    // this.msgs.push({ severity: 'error', summary: 'Error', detail: res.message });
                    setTimeout(() => { this.msgs = []; this.message = null; }, 2000);
            });
    }
    fileChangeEvent(fileInput: any) {
        const self = this;

        if (fileInput.target.files && fileInput.target.files[0]) {
            const reader = new FileReader();
            this.isEnable = true;
            this.isResult = false;
            reader.onload = function (e: any) {
                $('#preview').attr('src', e.target.result);
                self.file = fileInput.target.files[0];
            };

            reader.readAsDataURL(fileInput.target.files[0]);
        }
    }
}
