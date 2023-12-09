import { Component, Input } from '@angular/core';
import { NgbModal, NgbModalOptions } from '@ng-bootstrap/ng-bootstrap';
import { Product } from 'src/models/Product';
import { AddSalesComponent } from '../add-sales/add-sales.component';
import { SetPriceComponent } from '../set-price/set-price.component';
import { RestService } from '../rest.service';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent{
  delete_product: Product| null = null;;
  products = [
    {
      company: "Xiaomi Redmi",
      name:"Redmi Note 11S ",
      rating: 4.2,
      price: "17,198",
      features: "8GB/128GB\n6.43 inch) Display\n5000 mAh\nOcta Core\n108MP Rear Camera"
    },
    {
      company: "Samsung",
      name: "Samsung Galaxy A23",
      rating: 4.3,
      price: "18,999",
      features: "8GB/128GB\n(6.6 inch) Full HD+ Display\n5000 mAh\nOcta-core(EXYNOS) Processor\n108MP Rear Camera"
    },
    {
      company: "RealMe",
      name: "realme 10",
      price: "15,999",
      rating: 4.3,
      features: '8GB/128GB\n(6.4 inch) Full HD+ Display\n5000 mAh Battery\n50MP + 2MP\nMediatek Helio G99 Octa Core'
    },
    {
      company: "Oppo",
      name: "OPPO A77s",
      price: "17,999",
      features: "8GB/128GB\n(6.56 inch) HD+ Display\n50MP + 2MP Rear camera\n5000 mAh Battery\nQualcomm Snapdragon 680 Processor",
      rating: 4.26
    }
  ]
  constructor(private modal: NgbModal, private rest: RestService){

  }
  modalref:any;
  sales: number = 0
  recommended_price = 0
  price = 0
  comp_products: any[] = []
  error = false;
  errorMessage = ''
  @Input() product!:Product;
  openSetPrice(content:any){
    this.rest.getRecommendedPrice(this.product.id!).then(
      res =>{
        this.recommended_price = this.price = res.data.price
        this.comp_products = res.data.cp
        this.modalref = this.modal.open(content, { size: 'l' })
        this.error = false
      }
    )
    .catch(
      res =>{
        this.error = true
        this.errorMessage = "Please come back after some time."
        this.modalref = this.modal.open(content)
        
      }
    )
  }
  
  openAddSales(content: any){
    this.modalref =  this.modal.open(content)
  }

  addSales(event: any){
    event.preventDefault()
    this.rest.addSales(this.product.id!, this.sales).then(
      res =>
      this.modalref.close()
    )
  }

  setPrice(event: any) {
    event.preventDefault()
    this.rest.setPrice(this.product.id!, this.price).then(
      res =>
      this.modalref.close()
    )
  }

  openDeleteModal(content: any) {
    console.log(content)
    this.modalref = this.modal.open(content)
  }
  
      delete(event:any){
        event.preventDefault()
        this.rest.delete_product(this.product.id as string).then(
          res =>{
            this.modalref.close()
          }
         )
  
      }
}
