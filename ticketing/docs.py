question_list_get ="""
ادمین به تمام تیکت ها دسترسی دارد با پارام 
customer
به تیکت های کاربر مد نظر دسترسی دارد 
کاربر فقط به تیکت های خود دسترسی دارد
Ticket Model:
    title = عنوان
    auther = نویسنده
    body = متن تیکت
    date = تاریخ 
    type = نوع سوال اتخابی از گزینه های زیر 
        Choices_type =(
        ( '1','Financial'),
        ('2','Social'),
        ('3','holiday'),
        ('4','Others')
        )
        ticket_answer_obj: لیست پاسخ های این تیکت
        
params:
customer
ادمین با این پارام به تیکت های کاربر خاص دسترسی دارد
type
ادمین یا کاربر به تایپ های مد نظر خود از تیکت ها دسترسی دارد
date
بر اساس تاریخ ساخت تیکت ان ها را بعد ان تاریخ نشان می کند

"""

question_list_post ="""
کاربر تیکت  مد نظر خود را میسازد
Ticket Model:
{
    title = عنوان
    body = متن تیکت
    type = نوع سوال اتخابی از گزینه های زیر 
        Choices_type =(
        ( '1','Financial'),
        ('2','Social'),
        ('3','holiday'),
        ('4','Others')
        )
        به صورت پیش فرض 4 است
}
"""

answer_list_get ="""
برای ادمین اگر پارام 
question
باشد صرفا پاسخ  های این تیکت را بر می دارد
اگر نباشد کل پاسخ ها را برمیگرداند
اگر کابر باشد فقط میتواند به پاسخ های تیکت های خود دسترسی پیدا کند
params :
    question = id ticket
    date = 1 sort with date
TicketAnswer Model:
{
    question = ای دی تیکت مد نظر
    authern = نویسنده این پاسخ برای تیکت
    text = متن پاسخ تیکت
    date =تاریخ
}
"""

answer_list_post ="""
کاربر برای تیکت خود می تواند جواب دهد 
ادمین به کل تیکت ها می تواند جواب دهد 
"""


question_update_retrieve= """
کاربر فقط به تیکت خود دسترسی دارد 
ادمین به تمام تیکت ها دسترسی دارد
"""
question_update_update=""""
فقط کاربر میتواند تیکت خود را بروز رسانی کند
model update:

{
    "title": "title",
    "body": "body"
    "type": "type"

}

"""
question_update_destroy =""""
ادمین هر تیکت را میتواند حدف کند 
کاربر فقط تیکت های خود را حذف میکند
"""



answer_update_retrieve ="""
کاربر فقط به پاسخ خود دسترسی دارد 
ادمین به تمام پاسخ ها دسترسی دارد
"""
answer_update_update="""
فقط کاربر میتواند پاسخ خود را بروز رسانی کند
model update:

{
    "text": "text",
}

"""
answer_update_destroy ="""
ادمین هر پاسخ را میتواند حدف کند 
کاربر فقط پاسخ های خود را حذف میکند
"""