import { Component, OnInit } from '@angular/core';
import { RestService } from '../rest.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AddProductComponent } from '../add-product/add-product.component';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  constructor( private restService: RestService, private modal: NgbModal ){}
  products: any;
  ngOnInit(): void {
    this.products = this.restService.subject
  }

  open(){
    this.modal.open(AddProductComponent, { size: 'xl' });
  }

}
