import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { SharedModule } from '../../../core/modules/shared.module';

import { UploadComponent } from './upload.component';
// primeng
import { MessagesModule } from 'primeng/primeng';
import { GrowlModule } from 'primeng/primeng';
const routes = [
    {
        path     : 'upload',
        component: UploadComponent
    }
];

@NgModule({
    declarations: [
        UploadComponent
    ],
    imports     : [
        SharedModule,
        RouterModule.forChild(routes),
        MessagesModule,
        GrowlModule
    ],
    exports     : [
        UploadComponent
    ]
})

export class UploadModule
{
}
