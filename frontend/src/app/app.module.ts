import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RouterModule, Routes } from '@angular/router';
import 'hammerjs';
import { SharedModule } from './core/modules/shared.module';
import { AppComponent } from './app.component';
import { FuseMainModule } from './main/main.module';
import { FuseSplashScreenService } from './core/services/splash-screen.service';
import { FuseConfigService } from './core/services/config.service';
import { FuseNavigationService } from './core/components/navigation/navigation.service';
import { CompareModule } from './main/content/compare/compare.module';
import { UploadModule } from './main/content/upload/upload.module';
import { SerivceModule } from './services/service.module';
import { TranslateModule } from '@ngx-translate/core';
// primeng
import { MessagesModule } from 'primeng/primeng';
import { GrowlModule } from 'primeng/primeng';

const appRoutes: Routes = [
    {
        path: '**',
        redirectTo: 'compare'
    }
];

@NgModule({
    declarations: [
        AppComponent
    ],
    imports: [
        BrowserModule,
        HttpClientModule,
        BrowserAnimationsModule,
        RouterModule.forRoot(appRoutes),
        SharedModule,
        TranslateModule.forRoot(),
        FuseMainModule,
        MessagesModule,
        GrowlModule,
        CompareModule,
        UploadModule,
        SerivceModule
    ],
    providers: [
        FuseSplashScreenService,
        FuseConfigService,
        FuseNavigationService
    ],
    bootstrap: [
        AppComponent
    ]
})
export class AppModule {
}
