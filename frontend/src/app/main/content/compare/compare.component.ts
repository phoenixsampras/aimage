import { Component, ViewChild, ElementRef, ChangeDetectorRef } from '@angular/core';
import { Observable } from 'rxjs/Rx';
import { FuseTranslationLoaderService } from '../../../core/services/translation-loader.service';
import { ImageService } from '../../../services';
import { locale as english } from './i18n/en';
import { locale as turkish } from './i18n/tr';
import { Http } from '@angular/http';
import { RequestOptions } from '@angular/http';
import { SortablejsOptions } from 'angular-sortablejs';
import * as sortBy from 'sort-array';
declare let $: any;
@Component({
    selector: 'fuse-sample',
    templateUrl: './compare.component.html',
    styleUrls: ['./compare.component.scss']
})
export class CompareComponent {
    isLoading = false;
    isEnable = false;
    display= false;
    isResult = false;
    file: any;
    masksTag = [];
    result = [];
    select: any = {}
    masks = {};
    msgs = [];
    canSort = true;
    message: any;
    sortOption: SortablejsOptions = {}
    constructor(
        private translationLoader: FuseTranslationLoaderService,
        private imageService: ImageService,
        private forceView: ChangeDetectorRef,
        private http: Http) {
        this.translationLoader.loadTranslations(english, turkish);
        this.sortOption = {
            onUpdate:(event: any) => {
                console.log(event)
                console.log(this.result)
                this.isLoading = true;
                this.canSort = false;
                console.log(this.masks);
                this.checkOrderChange();
            },
            draggable: '.dragabble'
        }
    }
    sortResult() {
        this.result = sortBy(this.result,'order');
        this.forceView.detectChanges();
    }
    changeOrder(item) {
        let oldorder = item.order;
        item.order= item.newOrder;
        return new Promise(resolve => {
            this.imageService.changeOrder(item.input_id, oldorder, item.newOrder).subscribe(data => {
                resolve();
            })
        })
    }
    checkOrderChange() {
        var listChanged = [];
         Promise.all(this.result.map((item: any,index) => {
             return new Promise(resolve => {
                 
                if(this.masks[index] != item) {
                    console.log('changed', this.masks[index])
                    try {
                    item.newOrder = this.masks[index].order; }
                    catch(err) {
                        console.log('err', this.masks)
                    }
                    listChanged.push(item)
                }
                resolve();
             })
        })).then(() => {
            Promise
                .all(listChanged.map(item => this.changeOrder(item)))
                .then(() => {
                    this.isLoading = false;
                    this.saveMask();
                })
        })

    }
    saveMask() {
        this.sortResult()
        this.masks = Object.assign([], this.result);
        this.canSort =true;
        this.forceView.detectChanges();
        console.log('can sort')
    }
    onTapCompare() {
        this.isLoading = true;
        this.imageService.compare(this.file)
            .then(res => {
                this.result = res;
                this.saveMask();
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

            })
            .catch(error => {
                this.isLoading = false;
                console.error(error);
                this.message = error.message;
                    // this.msgs.push({ severity: 'error', summary: 'Error', detail: res.message });
                    setTimeout(() => { this.msgs = []; this.message = null; }, 2000);
            });
    }
    private resetResult() {
        this.result = []
    }
    fileChangeEvent(fileInput: any) {
        const self = this;
        this.resetResult();
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
    removeFromResult(item) {
        this.isLoading = true;
        console.log(this.isLoading)
        this.imageService.remove(
             item.input_id,
             item.order
        ).subscribe(data => {
            this.isLoading = false;
            let refreshResult = this.result.filter(r => r != item)
            this.result = refreshResult
            this.saveMask();
        })
    }
    reset() {
        this.isLoading = true
        this.imageService.reset(this.result[0].picture_id).subscribe(data => {
            this.isLoading = false;
            this.onTapCompare()
        })
    }
    showDialogTags(item) {
        this.select = item;
        this.masksTag = item.tags;
        this.display = true;
    }
 
    saveTag() {
        this.isLoading = true;
        this.imageService.editTag(this.select.id, this.masksTag).subscribe(response =>{
            this.select.tags = this.masksTag
            this.masksTag = [];
            this.isLoading = false;
        })
    }
}
