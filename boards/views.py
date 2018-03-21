from django.shortcuts import render,redirect
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from .forms import StudentLoginForm,studentForm,createHostelForm,createFloorForm,chooseRoomForm
from boards.models import Student,Hostel,Hostels
from django.db.models import Max, IntegerField
# Create your views here.

def home(request):
    return HttpResponse('Hello, World!')

def studentLogin(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            ob=Student.objects.get(usn=form.cleaned_data['usn'])
            if ob.room==None:
                request.session['usn']=form.cleaned_data['usn']
                return redirect('/bookHostel/')
            else:
                request.session['usn']=form.cleaned_data['usn']
                return redirect('/hostelBooked/')
    else:
        form = StudentLoginForm()
    pageContext='Student Hostel Booking'
    buttonText='Book'
    return render(request, 'formTemplate.html', {'form': form,'pageContext':pageContext, 'buttonText':buttonText})

def billNotPaid(request):
    return HttpResponseRedirect('/registerStudent/')

def registerStudent(request):
    if request.method == 'POST':
        form = studentForm(request.POST)
        if form.is_valid():
            form.setPriority()
            form.save()
            return HttpResponseRedirect('/studentLogin/')
        #else:
            #return HttpResponseRedirect('/billNotPaid/')
    else:
        form = studentForm()
    pageContext='Pay Hostel Bill'
    buttonText='Pay'
    return render(request, 'formTemplate.html', {'form': form,'pageContext':pageContext, 'buttonText':buttonText})

def createHostel(request):
    HostelFormSet=formset_factory(createHostelForm, max_num=1)
    FloorFormSet=formset_factory(createFloorForm, min_num=1)
    if request.method == 'POST':
        hostelFormSet = HostelFormSet(request.POST, request.FILES, prefix='hostel')
        floorFormSet = FloorFormSet(request.POST, request.FILES, prefix='floor')
        if floorFormSet.is_valid() and hostelFormSet.is_valid():
            hostel=0
            hsize=0
            for host in hostelFormSet:
                h=Hostels(hname=host.cleaned_data['hname'],gender=host.cleaned_data['gender'],year=host.cleaned_data['year'],size=hsize,asize=hsize,)
                h.save()
            for floor in floorFormSet:
                for size in range(3,0,-1):
                    roomblocks=floor.cleaned_data[('res'+str(size))].split(',')
                    for block in roomblocks:
                        rrange=block.split('-')
                        if len(rrange)> 1:
                            for room in range(int(rrange[0]),int(rrange[1])):
                                roomdet=h.hosteldetails.create(roomn=room,size=size,asize=size,status=3,floor=floor.cleaned_data['Floor'])
                                roomdet.save()
                                hsize+=1
                        else:
                            roomdet=h.hosteldetails.create(roomn=int(rrange[0]),size=size,asize=size,status=3,floor=floor.cleaned_data['Floor'])
                            roomdet.save()
                            hsize+=1
            h.asize=h.size=hsize
            h.save()
            return HttpResponseRedirect('/admin/')
        else:
            pass
    else:
        hostelFormSet = HostelFormSet(prefix='hostel')
        floorFormSet = FloorFormSet(prefix='floor')
    return render(request, 'createHostel.html', {'hostelFormSet': hostelFormSet, 'floorFormSet':floorFormSet,})

def bookHostel(request):
    if request.method=='POST':
        form=chooseRoomForm(request.POST)
        if form.is_valid():
            s=Student.objects.get(usn=request.session['usn'])
            r=form.cleaned_data['room']
            s.room=r
            r.asize=r.asize-1
            s.hostel.asize=s.hostel.asize-1
            if r.asize<1:
                r.status=0
            r.save()
            s.hostel.save()
            s.save()
            return redirect('/hostelBooked/')
        else:
             return redirect('/studentLogin/')
    else:
        s=Student.objects.get(usn=request.session['usn'])
        h=s.hostel
        fl=h.hosteldetails.all().aggregate(Max('floor',output_field=IntegerField()))['floor__max']+1
        f={}
        string='<table class="table table-bordered table-responsive">\n'
        for i in range(1,fl):
            f[i]=h.hosteldetails.filter(floor=i)
            string+='<tr>\n<th scope="row"> Floor '+str(i)+'</th>'
            for room in f[i]:
                col=''
                if room.status==0:
                    col='red'
                elif room.status==1:
                    col='gray'
                elif room.status==2:
                    col='aqua'
                else:
                    col='inherit'
                string+='<td bgcolor='+col+'> '+str(room.roomn)+'<br>Available Size: '+str(room.asize)+'</td>'
            string+='\n</tr>'
        string+='</table>'
        pageContext='Choose From Rooms Available'
        buttonText='Choose'
        roomc=chooseRoomForm()
        roomc.roomBlock(h,s.billcategory)
    return render(request,'tableTemplate.html',{'hostel':string,'form':roomc,'pageContext':pageContext, 'buttonText':buttonText})

def printRecipt(request):
    pageContext='Hostel Booking Confirmed'
    s=Student.objects.get(usn=request.session['usn'])
    return render(request, 'printTemplate.html', {'student': s,'pageContext':pageContext})
