import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { AddProductComponent } from './add-product/add-product.component';
import { StatisticsComponent } from './statistics/statistics.component';
import { CompComponent } from './comp/comp.component';
import { CompetitiveProductComponent } from './competitive-product/competitive-product.component';

const routes: Routes = [
  { path: "", component: DashboardComponent },
  {path: "stats/:id", component:StatisticsComponent},
  {path:'competitor-analysis/:id', component: CompetitiveProductComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
