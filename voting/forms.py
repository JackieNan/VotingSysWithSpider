from django import forms
from .models import *
from account.forms import FormSettings


class VoterForm(FormSettings):
    class Meta:
        model = Voter
        fields = ['phone']
        labels = {
            'phone': '电话号码',
        }


class PositionForm(FormSettings):
    class Meta:
        model = Position
        fields = ['name', 'max_vote']
        labels = {
            'name': '姓名',
            'max_vote': '最大投票数',
        }


class CandidateForm(FormSettings):
    class Meta:
        model = Candidate
        fields = ['fullname', 'bio', 'position', 'photo']
        labels = {
            'fullname': '全名',
            'bio': '个人简介',
            'position': '职位',
            'photo': '头像',
        }
