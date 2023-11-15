from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
alphanumeric = RegexValidator(r'^[0-9a-zA-Z ]*$', 'Solo caratteri alfanumerici.')

class Progetto(models.Model):

    STATI = [
        ('INCORSO', 'In corso'),
        ('COMPLETATO', 'Completato'),
    ]

    titolo = models.CharField(max_length=100)
    descrizione = models.TextField()
    data_creazione = models.DateTimeField(auto_now_add=True)
    data_modifica = models.DateTimeField(auto_now=True)
    autore = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="autore")
    link_progetto = models.CharField(max_length=100, blank=True)
    stato = models.CharField(max_length=100)
    tags = models.ManyToManyField("Tag", blank=True)
    contributi = models.ManyToManyField("Contributo", blank=True)

    def __str__(self):
        return self.titolo
    
    class Meta:
        verbose_name_plural = "Progetti"

class Sviluppo(models.Model):

    STATI = [
        ('DAFARE', 'Da fare'),
        ('INCORSO', 'In corso'),
        ('COMPLETATO', 'Completato'),
    ]

    progetto = models.ForeignKey(Progetto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descrizione = models.TextField()
    data_inizio = models.DateField(auto_now_add=False, blank=True, null=True)
    data_fine = models.DateField(auto_now_add=False, blank=True, null=True)
    stato = models.CharField(max_length=100)
    responsabile = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = "Sviluppi"

class Contributo(models.Model):

    RUOLI = [
        ("Relatore", "Relatore"),
        ("Responsabile scientifico", "Responsabile scientifico"),
        ("Collaboratore", "Collaboratore"),
    ]

    contributore = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    ruolo = models.CharField(max_length=100)

    def __str__(self):
        return self.contributore.username
    
    class Meta:
        verbose_name_plural = "Contributi"

class Immagine(models.Model):
    progetto = models.ForeignKey(Progetto, on_delete=models.CASCADE, blank=True, null=True)
    img = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.img.name
    
    class Meta:
        verbose_name_plural = "Immagini"

class Tag(models.Model):
    nome = models.CharField(max_length=100, unique=True, validators=[alphanumeric])

    def __str__(self):
        return self.nome