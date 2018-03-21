import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { SharedModule } from '../../../core/modules/shared.module';

import { CompareComponent } from './compare.component';
import { FileUploadModule } from 'primeng/fileupload';
// primeng
import { MessagesModule } from 'primeng/primeng';
import { GrowlModule } from 'primeng/primeng';
const routes = [
    {
        path: 'compare',
        component: CompareComponent
    }
];

@NgModule({
    declarations: [
        CompareComponent
    ],
    imports: [
        SharedModule,
        RouterModule.forChild(routes),
        FileUploadModule,
        MessagesModule,
        GrowlModule
    ],
    exports: [
        CompareComponent
    ]
})

export class CompareModule {
}
