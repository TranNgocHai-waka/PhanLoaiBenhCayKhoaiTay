import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { Result } from '../interfaces/result.interface';

@Injectable({
  providedIn: 'root'
})
export class ResultServiceService {
  private readonly baseURL = "http://localhost:5000/"

  constructor(private httpClient: HttpClient) { }

  public getAllResult(): Observable<any> {
    var param = JSON.parse(localStorage.getItem("userInfo")).UserID
    return this.httpClient.get<any>(this.baseURL + "get/"+ param )
  }
  public deleteResult(id:number): Observable<any> {
    return this.httpClient.delete<any>(this.baseURL + "delete_result_by_id/" +id)
  }
  public addResult(UserID: number, LinkImg:string, Img: any) {
    var param = `results?UserID=${UserID}&LinkImg=${LinkImg}`
    return this.httpClient.post<any>(this.baseURL + param,Img)
  }

  public getAllResultManagement(): Observable<any> {
    var param = JSON.parse(localStorage.getItem("userInfo")).UserID
    return this.httpClient.get<any>(this.baseURL + "get/manager/"+ param )
  }

  // public getSearchAll(dob: string, sick: string): Observable<any> {
  //   var id = JSON.parse(localStorage.getItem("userInfo")).UserID
  //   //var param = `search?id=${id}&Dob=${dob}&Sick=${sick}&Accuracy=${accuracy}`
  //    // return this.httpClient.get<any>(this.baseURL+param)
  //   return this.httpClient.get<any>(this.baseURL + "get/search?id="+ id + "&dob=" + dob + "&sick=" + sick)
  // }
  // public getSearchAll(dob: string, sick: string) {
  //   var body =null
  //   var id = JSON.parse(localStorage.getItem("userInfo")).UserID
  //   var param = `get/search/?id=${id}&dob=${dob}&sick=${sick}`
  //     return this.httpClient.get<any>(this.baseURL+param, body)
  // }

  public getSearchAll(dob: string, sick: string): Observable<any> {
    var id = JSON.parse(localStorage.getItem("userInfo")).UserID
    if(dob != "" && sick == "") {
      return this.httpClient.get<any>(this.baseURL + "get/searchDOB/?id=" + id + "&dob=" +dob )
    } else if(dob == "" && sick != "") {
      return this.httpClient.get<any>(this.baseURL + "get/searchSick/?id=" + id +"&sick=" + sick )
    } else if(dob != "" && sick != ""){
      return this.httpClient.get<any>(this.baseURL + "get/search/?id=" + id + "&dob=" +dob +"&sick=" + sick )
    } else {
      return this.httpClient.get<any>(this.baseURL + "get/manager/"+ id )
    }
    
  }
}
