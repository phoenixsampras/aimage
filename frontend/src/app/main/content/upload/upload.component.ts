import { Component } from '@angular/core';
import { FuseTranslationLoaderService } from '../../../core/services/translation-loader.service';
import { ImageService } from '../../../services';

import { locale as english } from './i18n/en';
import { locale as turkish } from './i18n/tr';
import { Message } from 'primeng/components/common/api';
import { MatDialog } from '@angular/material';
declare let $: any;
@Component({
    selector: 'my-upload',
    templateUrl: './upload.component.html',
    styleUrls: ['./upload.component.scss']
})
export class UploadComponent {
    isLoading = false;
    isEnable = false;
    file: any;
    isResult = false;
    result = [];
    msgs: Message[] = [];
    message: any;
    constructor(private imageService: ImageService,
        private translationLoader: FuseTranslationLoaderService,
        public dialog: MatDialog) {
        this.translationLoader.loadTranslations(english, turkish);
    }
    onTapCompare() {
        this.isLoading = true;
        this.msgs = [];
        this.imageService.compare(this.file, true)
            .then(res => {
                this.isLoading = false;
                this.result = res.searchResult;
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
            })
            .catch(error => {
                this.isLoading = false;
                console.error(error);
                this.message = error.message;
                this.msgs.push({ severity: 'error', summary: 'Error', detail: error.message });
                setTimeout(() => { this.msgs = []; this.message = null; }, 2000);
            });
    }
    fileChangeEvent(fileInput: any) {
        const self = this;

        if (fileInput.target.files && fileInput.target.files[0]) {
            const reader = new FileReader();
            this.isEnable = true;
            this.isResult = false;
            // const formData = new FormData();

            // formData.append('file[]', fileInput.target.files[0]);
            reader.onload = function (e: any) {
                self.file = fileInput.target.files[0];
                $('#preview-upload').attr('src', e.target.result);
            };

            reader.readAsDataURL(fileInput.target.files[0]);
        }
    }
}
