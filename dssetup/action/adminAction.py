#coding=utf-8
from dssetup.forms import UserForm,GroupForm,AuthorityForm,ZoneForm,DomainFormForm
from django.shortcuts import render 
from django.http import HttpResponseRedirect
from dssetup.service import adminService

def show_object(request,obj):
    """
       返回要展示在列表中的obj_list

       obj: 表示需要显示哪个物体的列表 user 还是group

    """
    return render(request,"index.html",{
                  "obj_list":adminService.getAllObject(obj),
                  "obj":obj,                     
                })
 
 
def delete_object(request,Id,obj):
    """
       删除Id对应的物体

       obj表示需要删除哪个物体 group 还是user...

    """
    adminService.deleteObjectById(obj, Id)
    return HttpResponseRedirect("/admin/"+obj+"/")

 
def add_object(request,obj):
    """
      创建对象

      obj:表示需要创建哪个对象 group 还是user 还是 auth 。...

    """
    if(request.POST):
        form = __generateForm(post=request.POST,obj=obj) #生成obj对应的表单
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect("/admin/"+obj)
        
        else:
            return render(request,"add.html",{"form":form,"obj":obj})
    else:
        form = __generateForm(obj=obj)
        return render(request,"add.html",{"form":form,"obj":obj})
 
def edit_object(request,Id,obj):
    """
        编辑对象

        obj：表示需要编辑哪个对象

    """
    instance_ = adminService.getObjectById(obj, Id) 
    if(request.POST):
        form = __generateForm(post=request.POST,instance_=instance_,obj=obj)#生成相应的表单       
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect("/admin/"+obj)
        else: 
            return render(request,"edit.html",{"form":form,"obj":obj,"id":Id})

    else:
        form = __generateForm(instance_=instance_,obj=obj)         
        return render(request,"edit.html",{"form":form,"obj":obj,"id":Id})

def __generateForm(obj,post=None,instance_=None):
    """
      根据参数生成不同需求的表单

      obj:标识需要生成哪种对象的表单
      post:标识是否有post数据过来
      instance_:标识是否是edit表单
    """
    if(obj == "user"):
        form = UserForm(data=post,instance=instance_)
    elif(obj == "group"):
        form = GroupForm(data=post,instance=instance_)
    elif(obj == "authority"):
        form = AuthorityForm(data=post,instance=instance_)
    elif(obj == "zone"):
        form = ZoneForm(data=post,instance=instance_)
    elif(obj =="domain"):
        form = DomainFormForm(data=post,instance=instance_)
    return form

def addUserToGroup(request,Id):
    """ 
       批量添加用户到群组里面

       Id:表示权限组的id     
    """
    if(request.POST):
        for userId in request.POST.getlist("userIds"):
            adminService.addUserIntoGroup(Id, userId)
        return render(request,"/admin/group/")
    else:
        return render(request,"user_into_group.html",{"users":adminService.getUsersNotInThisGroup(Id),"Id":Id})
