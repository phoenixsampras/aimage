import { HttpModule } from '@angular/http';
import { NgModule } from '@angular/core';
import { ApiService } from './api.service';
import { ImageService } from './image.service';

@NgModule({
    imports: [
        HttpModule
    ],
    exports: [],
    declarations: [],
    providers: [
        ApiService,
        ImageService
    ],
})
export class SerivceModule { }
