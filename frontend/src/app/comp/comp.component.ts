import { Component } from '@angular/core';

@Component({
  selector: 'app-comp',
  templateUrl: './comp.component.html',
  styleUrls: ['./comp.component.css']
})
export class CompComponent {
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
}
