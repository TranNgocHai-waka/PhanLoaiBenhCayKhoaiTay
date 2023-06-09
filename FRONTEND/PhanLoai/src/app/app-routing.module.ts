import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ClassifyComponent } from './classify/classify.component';
import { LoginComponent } from './login/login.component';
import { AuthGuard } from './service/auth.guard';
import { ManagerComponent } from './manager/manager.component';
import { InforComponent } from './infor/infor.component';
import { RegisterComponent } from './register/register.component';

const routes: Routes = [
  {path: '', redirectTo: 'login', pathMatch: 'full'},
  {path: 'login', component: LoginComponent},
  {path: 'classify', component: ClassifyComponent, canActivate: [AuthGuard]},
  {path: 'manager', component: ManagerComponent, canActivate: [AuthGuard]},
  {path: 'infor', component: InforComponent, canActivate: [AuthGuard]},
  {path: 'register', component: RegisterComponent, canActivate: [AuthGuard]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class AppRoutingModule { }
