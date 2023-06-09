import { Binary } from '@angular/compiler';
import { ChangeDetectorRef, Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { DialogService } from 'primeng/dynamicdialog';
import { Result } from '../interfaces/result.interface';
import { User } from '../interfaces/user.interface';
import { ResultServiceService } from '../service/result-service.service';
import { ToastMessageService } from '../service/toast-message.service';
import { UserServiceService } from '../service/user-service.service';
import { UserUpdateComponent } from '../user-update/user-update.component';

@Component({
  selector: 'app-manager',
  templateUrl: './manager.component.html',
  styleUrls: ['./manager.component.css'],
  providers: [DialogService]
})
export class ManagerComponent {
  constructor (private router: Router,
    private messageService: MessageService,
    private toastMessageService: ToastMessageService,
    private resultService: ResultServiceService,
    public dialogService: DialogService,
    public fb: FormBuilder,
    private cdr: ChangeDetectorRef,
    private userService: UserServiceService) {}
  public userList: Result[] = [];
  public list: User[]=[];
  uploadForm: FormGroup;
  formManagement: FormGroup;
  imageURL: string = '';
  public userInfor = JSON.parse(localStorage.getItem("userInfo")).User
  // public managerInfor = JSON.parse(localStorage.getItem("managerInfor")).Result
  ngOnInit(): void {
    this.getAllResultManagement()
    this.uploadForm = this.fb.group({
      avatar: [null],
    })

    this.formManagement = this.fb.group({
        dob: ['', Validators.required],
        sick: ['', Validators.required],
        accuracy: ['', Validators.required],
  
      });
  }
   
  showPreview(event) {
    const file = (event.target as HTMLInputElement).files[0];
    this.uploadForm.patchValue({
      avatar: file
    });
    this.uploadForm.get('avatar').updateValueAndValidity()
    const reader = new FileReader();
    reader.onload = () => {
      this.imageURL = reader.result as string;
    }
    reader.readAsDataURL(file)
  }

  getAllResultManagement(){
    this.resultService.getAllResultManagement().subscribe((data: any) => {
      this.userList = [];
      console.log(data)
      this.userList = data
      this.cdr.detectChanges()
    });
    
  }
  logout() {
    this.router.navigateByUrl("login")
  }

  deleteResult1(ResultID:number) {
    this.toastMessageService.showConfirmDeleteSwal("Kết quả",'này').then(result => {
      if (result.isConfirmed) {
        this.resultService.deleteResult(ResultID).subscribe({next: res => {
          console.log(res)
            this.getAllResultManagement();
        }})
        this.messageService.add({severity:'success', summary: 'Thành công', detail: 'Xóa thành công kết quả'});
      }

    })
  }

  search() {
    //this.newItemEvent.emit(userId);
    
    let dob = this.formManagement.controls["dob"].value;
    let sick = this.formManagement.controls["sick"].value;
    // let accuracy = this.formManagement.controls["accuracy"].value;
    this.resultService.getSearchAll(dob,sick).subscribe((data: any) => {
      this.userList = [];
      console.log(data)
      this.userList = data
      this.cdr.detectChanges()
    })
  }
  
}
