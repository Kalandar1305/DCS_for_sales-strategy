import { Component, OnInit } from '@angular/core';
import { RestService } from '../rest.service';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.css']
})
export class StatisticsComponent implements OnInit {
  image1=""
  image2=""
  product_id=""
  aspectImages = []
  negReviews:{content: string, title: string}[] = []
  posReviews:{content: string, title: string}[] = []
  reviews : {content: string, title: string}[] = []
  constructor(private rest: RestService, private activated: ActivatedRoute){

  }
  status = 'negative'
  ngOnInit(): void {
      this.activated.params.subscribe(
        params =>{
          this.product_id = params['id']
          this.rest.getGraphs(this.product_id).then(
            res =>{
              this.image1 = "http://172.17.0.2:5000/"+res.data.image1
              this.image2 = "http://172.17.0.2:5000/"+ res.data.image2
            }
          )
          this.rest.getNegativeReviews(this.product_id).then(res =>{
            this.negReviews = res.data
            this.reviews = this.negReviews
          })
          this.rest.getPositiveReviews(this.product_id).then(res =>{
            this.posReviews = res.data
          })
          this.rest.getAspectSentiment(this.product_id).then(
            res => {
              this.aspectImages = res.data.images
            }
          )
        }
      )
  }

  change(){
    if (this.status === 'negative'){
      this.reviews=this.negReviews
    }
    else{
      this.reviews = this.posReviews
    }
  }

}
