import { Component } from '@angular/core';
import { Product } from 'src/models/Product';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { RestService } from '../rest.service';

@Component({
  selector: 'app-add-product',
  templateUrl: './add-product.component.html',
  styleUrls: ['./add-product.component.css']
})
export class AddProductComponent {
  constructor(private modal: NgbActiveModal, private rest: RestService){}
  product: Product = {
    name: "",
    price: 0,
    min_price: 0,
    max_price: 0,
    urls: {
        flipkartURL: "",
        amazonURL: ""
    },
    type: "laptop"
  }
  submit(event: any){
    event.preventDefault();
    console.log(this.product)
    this.rest.add_product(this.product).then(
      res => {
        console.log("from component",res)
        this.modal.close()
        this.product = {
          name: "",
          price: 0,
          min_price: 0,
          max_price: 0,
          urls: {
              flipkartURL: "",
              amazonURL: ""
          },
          type: ''
        }
      }
    )
    .catch(err => console.log(err))
  }
}
