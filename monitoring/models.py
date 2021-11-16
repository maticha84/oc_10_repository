from django.db import models

from softdesk_project import settings


class Project(models.Model):
    BACKEND = "BACK-END"
    FRONTEND = "FRONT-END"
    IOS = "IOS"
    ANDROID = "ANDROID"

    TYPE_CHOICES = [
        (BACKEND, 'back-end'),
        (FRONTEND, 'front-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    ]
    title = models.CharField(max_length=200, verbose_name='Titre')
    description = models.CharField(max_length=5000, verbose_name='Description')
    type = models.CharField(max_length=200, verbose_name='Type de projet', choices=TYPE_CHOICES)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Contributor(models.Model):
    AUTHOR = 'AUTHOR'
    CONTRIBUTOR = 'CONTRIBUTOR'

    CHOICES = [
        (AUTHOR, 'Auteur'),
        (CONTRIBUTOR, 'Contributeur'),
    ]
    contributor = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_contributor')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='project_contributor')
    role = models.CharField(max_length=30, choices=CHOICES, verbose_name='role')



class Issue(models.Model):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    BUG = "BUG"
    IMPROVEMENT = "IMPROVEMENT"
    TASK = "TASK"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

    PRIORITY_CHOICES = [
        (LOW, 'Faible'),
        (MEDIUM, 'Moyenne'),
        (HIGH, 'Elevée'),
    ]

    TAG_CHOICES = [
        (BUG, "Bug"),
        (IMPROVEMENT, "Amélioration"),
        (TASK, "Tâche"),
    ]

    STATUS_CHOICES = [
        (TODO, "A faire"),
        (IN_PROGRESS, "En cours"),
        (COMPLETED, "Terminé"),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    desc = models.CharField(max_length=5000, verbose_name="Description")
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, verbose_name="Projet")
    tag = models.CharField(max_length=30, verbose_name="Tag", choices=TAG_CHOICES)
    priority = models.CharField(max_length=30, verbose_name="Priorité", choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=30, verbose_name="Statut", choices=STATUS_CHOICES)

    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='author',
                                    verbose_name='Auteur')
    assignee_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True,
                                      related_name='assignee', verbose_name='Assigné à')

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')



class Comment(models.Model):
    description = models.CharField(max_length=5000, verbose_name="Description")
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, verbose_name="Auteur")
    Issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
