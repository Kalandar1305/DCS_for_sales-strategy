import { Component, Input } from '@angular/core';
import { RestService } from '../rest.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-add-sales',
  templateUrl: './add-sales.component.html',
  styleUrls: ['./add-sales.component.css']
})
export class AddSalesComponent {
  constructor(private rest: RestService, private modal: NgbActiveModal){}
  @Input() week: number = 1;
  @Input() product_id: string = "";
  sales = 0

  submit(){
    this.rest.addSales(this.product_id, this.sales).then(
      res =>
      this.modal.close()
    )
  }
}
