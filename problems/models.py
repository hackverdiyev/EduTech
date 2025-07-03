from django.db import models
from base.models import Account

class Problem(models.Model):
    source_problem = models.CharField(max_length = 300)
    problem_subject = models.CharField(max_length = 20)
    problem_context_img = models.ImageField(upload_to = 'problems/', null = True, blank = True)
    problem_context = models.CharField(max_length = 10000, blank = True)
    problem_views = models.IntegerField(default = 0)
    pub_date = models.DateTimeField(auto_now_add = True)
    show_problem = models.BooleanField(default = False)
    have_solution = models.BooleanField(default = False)
    user_added = models.ForeignKey(Account, on_delete=models.CASCADE)
    def __str__(self):
        return self.source_problem

class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    solution_path_video = models.FileField(upload_to='solutions/', blank=True)
    solution_path_img = models.ImageField(upload_to='solutions/', blank=True)
    solution_cont = models.CharField(max_length=200000, blank=True)
    user_solved = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.problem.source_problem

class ReportedProblem(models.Model):
    problem_reported = models.ForeignKey(Problem, on_delete=models.CASCADE)
    checkbox_problem = models.BooleanField(default = False)
    checkbox_solution = models.BooleanField(default = False)
    checkbox_content = models.BooleanField(default = False)
    checkbox_chat = models.BooleanField(default = False)
    other = models.CharField(max_length=1000, blank=True)
    def __str__(self):
        return self.problem.source_problem

class Chat(models.Model):
    message = models.CharField(max_length = 10000)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user_added = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.problem.source_problem