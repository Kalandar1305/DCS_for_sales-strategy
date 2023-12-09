import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ProductComponent } from './product/product.component';
import { NavbarComponent } from './navbar/navbar.component';
import { AddProductComponent } from './add-product/add-product.component';
import { FormsModule } from '@angular/forms';
import { SetPriceComponent } from './set-price/set-price.component';
import { AddSalesComponent } from './add-sales/add-sales.component';
import { StatisticsComponent } from './statistics/statistics.component';
import { CompComponent } from './comp/comp.component';
import { CompetitiveProductComponent } from './competitive-product/competitive-product.component';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    ProductComponent,
    NavbarComponent,
    AddProductComponent,
    SetPriceComponent,
    AddSalesComponent,
    StatisticsComponent,
    CompComponent,
    CompetitiveProductComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
