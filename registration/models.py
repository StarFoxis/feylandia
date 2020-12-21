from django.db import models
from django.contrib.auth.models import User

class SkillModel(models.Model):
    name = models.CharField('Название', max_length=100)
    desc = models.TextField('Описание')
    required_level = models.PositiveSmallIntegerField('Требуемый уровень', default=0)
    required_mana = models.PositiveSmallIntegerField('Требуемая мана', default=10)
    # Возможно стоит добавить поля с путем для скрипта

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Умение'
        verbose_name_plural = 'Умения'
        ordering = ['name',]

class StyleModel(models.Model):
    name = models.CharField('Название класса', max_length=100)
    desc = models.TextField('Описание')
    skill = models.ManyToManyField(SkillModel, verbose_name='Скилы')

    def __str__(self):
        return self.name

    def skill_all(self):
        return ', '.join([obj.name for obj in self.skill.all()])
    
    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
        ordering = ['name',]

class SkinModel(models.Model):
    style = models.ForeignKey(StyleModel, on_delete=models.CASCADE, verbose_name='Класс', default=1)
    name = models.CharField('Название', max_length=100)
    image = models.ImageField('Изображение', upload_to='skins/')
    cost = models.PositiveIntegerField('Стоимость', default=1000)
    # В будущем стоит добавить для скинов баффы
    # Наложить требуемый уровень на скин

    def __str__(self):
        return f'{self.name}, {self.cost}'
    
    class Meta:
        verbose_name = 'Скин'
        verbose_name_plural = 'Скины'
        ordering = ['name',]

class PersonModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    style = models.ForeignKey(StyleModel, on_delete=models.CASCADE, verbose_name='Класс', default=1)
    skin = models.ForeignKey(SkinModel, null=True, on_delete=models.SET_NULL, verbose_name='Скин')
    level = models.PositiveSmallIntegerField('Уровень', default=0)
    health = models.PositiveSmallIntegerField('Здоровье', default=100)
    mana = models.PositiveSmallIntegerField('Мана', default=50)
    coins = models.PositiveIntegerField('Монеты', default=0)
    active = models.BooleanField('Активный персонаж', default=False)

    def __str__(self):
        return f'Пользователь: {self.user} Класс {self.style}'

    class Meta:
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонажи'
        ordering = ['user__username', 'style',]

# class PersonsModel(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
