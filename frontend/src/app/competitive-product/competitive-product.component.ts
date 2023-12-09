import { Component, OnInit } from '@angular/core';
import { RestService } from '../rest.service';
import { ActivatedRoute } from '@angular/router';
import { Product } from 'src/models/Product';

@Component({
  selector: 'app-competitive-product',
  templateUrl: './competitive-product.component.html',
  styleUrls: ['./competitive-product.component.css']
})
export class CompetitiveProductComponent implements OnInit{
  products: any[]= []
  id = ''
  product:any
  constructor(private rest:RestService, private activatedRoute: ActivatedRoute) {

  }
  ngOnInit(): void {
    this.activatedRoute.params.subscribe((params) =>{
      this.id = params['id']
      this.rest.getCompetitiveProducts(this.id).then((data) =>{
        this.products = data.data['products']
        this.product = this.rest.get_product_details(this.id)
      })
  })
  }

}
