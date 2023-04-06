import { Binary } from '@angular/compiler';
import { ChangeDetectorRef, Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
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
  imageURL: string = '';
  public userInfor = JSON.parse(localStorage.getItem("userInfo")).User
  ngOnInit(): void {
    //this.getAllResult()
    this.uploadForm = this.fb.group({
      avatar: [null],
    })
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

  getAllResult(){
    this.resultService.getAllResult().subscribe((data: any) => {
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
            this.getAllResult();
        }})
        this.messageService.add({severity:'success', summary: 'Thành công', detail: 'Xóa thành công kết quả'});
      }

    })
  }
  userEdit(id: number) {
    this.dialogService.open(UserUpdateComponent, {
      header: "Chỉnh sửa thông tin người dùng",
      width: "40%",
      data: {
        type: 'edit',
        id: id
      }
    });
  }
  

  manager() {
    let userid = this.userInfor.UserID
    let linkImg = "http.com"
    let img = this.uploadForm.controls["avatar"].value
    let formData = new FormData
    formData.append("file",img)
    console.log(img)
    
    this.resultService.addResult(userid, linkImg, formData).subscribe({
      next: (data:any )=> {
        console.log(data)
        this.getAllResult()
        if(data.UserID != null) {
          this.messageService.add({severity:'success', summary:'Success', detail: 'Phân loại thành công'})
        }
      },error: error => {
        this.messageService.add({severity:'error', summary: 'Error', detail: 'Lỗi trong quá trình phân loại'});
      }
    })

  }
  
}
