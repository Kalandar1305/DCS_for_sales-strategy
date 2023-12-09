import { Injectable } from '@angular/core';
import axios, { Axios } from 'axios';
import { BehaviorSubject } from 'rxjs';
import { Product } from 'src/models/Product';

@Injectable({
  providedIn: 'root'
})
export class RestService {
  httpClient: Axios;
  products: Product[] = []
  constructor() {
    this.httpClient = axios.create({
      baseURL: 'http://172.17.0.2:5000',
    });

    this.get_products()
  }

  subject = new BehaviorSubject(this.products)

  get_products() {
    return this.httpClient.get('get_products').then(
      res =>{
        this.products = res.data as Product[]
        console.log(res.data.length)
        this.subject.next(this.products)
      }
    )
  }

  add_product(product: Product) {
    return this.httpClient.post("add_product", product).then(
      (res) =>{
        this.products.push(res.data as Product)
        this.subject.next(this.products)
        return res
      }
    )
  }

  setPrice(product_id: string, price: number) {
    return this.httpClient.post("set_price", { product_id, price })
  }

  addSales(id: string, sales: number) {
    return this.httpClient.post("add_sales", { id, sales })
  }

  getRecommendedPrice(product_id: string) {
    return this.httpClient.get("get_predicted_price/" + product_id)
  }

  getGraphs(product_id: string) {
    return this.httpClient.get('graphs/' + product_id,)
  }

  getNegativeReviews(product_id: string) {
    return this.httpClient.get('negative_reviews/' + product_id)
  }
  getPositiveReviews(product_id: string) {
    return this.httpClient.get('positive_reviews/' + product_id)
  }
  getCompetitiveProducts(product_id: string) {
    return this.httpClient.get("competitive_products/" + product_id)
  }

  delete_product(product_id:string){
    return this.httpClient.delete('delete-product/' + product_id).then(
      res =>{
        this.products = this.products.filter((item) => item.id != product_id)
        this.subject.next(this.products)
        return res
      }
    )
  }

  getAspectSentiment(id:string){
    return this.httpClient.get('/aspect-sentiment/'+id)
  }

  get_product_details(product_id:string){
    let product;
    this.products.forEach((item) =>{
      if( item.id == product_id)
      product = item
    } )

    return product
  }
}
