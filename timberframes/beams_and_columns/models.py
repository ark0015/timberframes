from django.db import models

# from django.contrib import admin

# Create your models here.


class Wood_Type(models.Model):
    """Things needed to make up a wood type

    Parameters
    ----------
    lumber_types : glulam, dimensional, uncut (?)
        Drop-down or Radial button
    grade
        Drop-down or Radial button
    size : Different tables for (2-4") and (5"x5" or larger)
        Drop-down or Radial button
    E : modulus of elasticity (psi)
        * Short Float
        * Include units with drop-down
    E_min : minimum modulus of elasticity (psi)
        * Short Float
        * Include units with drop-down
    G : specific gravity
        * Short Float
        * Include units with drop-down
    F_v : design shear parallel to grain (psi)
        * Short Float
        * Include units with drop-down
    F_c : design compression parallel to grain (psi)
        * Short Float
        * Include units with drop-down
    F_c_perp : design compression perperdicular to grain (psi)
        * Short Float
        * Include units with drop-down
    F_b : design bending (psi)
        * Short Float
        * Include units with drop-down
    F_t : design tension parallel to grain (psi)
        * Short Float
        * Include units with drop-down
    """

    wood_name = models.CharField(max_length=200)
    # lumber_type = models.ForeignKey('Lumber_Type',on_delete=models.CASCADE)
    # grade = models.ForeignKey('Lumber_Grade',on_delete=models.CASCADE)
    # size = models.ForeignKey('Lumber_Size',on_delete=models.CASCADE)
    E = models.DecimalField(max_digits=7, decimal_places=2)
    E_min = models.DecimalField(max_digits=7, decimal_places=2)
    G = models.DecimalField(max_digits=7, decimal_places=2)
    F_v = models.DecimalField(max_digits=7, decimal_places=2)
    F_c = models.DecimalField(max_digits=7, decimal_places=2)
    F_c_perp = models.DecimalField(max_digits=7, decimal_places=2)
    F_b = models.DecimalField(max_digits=7, decimal_places=2)
    F_t = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.wood_name


class Wood_Choice(models.Model):
    """
    Parameters
    ----------
    lumber_types : glulam, dimensional, uncut (?)
        * Drop-down or Radial button
    grade
        * Drop-down or Radial button
    size : Different tables for (2-4") and (5"x5" or larger)
        - breadth
            * Short Float
            * Include units with drop-down
        - depth
            * Short Float
            * Include units with drop-down
    """

    wood_choice = models.ForeignKey(Wood_Type, on_delete=models.CASCADE)
    # lumber_type = models.ForeignKey('Lumber_Type',on_delete=models.CASCADE)
    # grade = models.ForeignKey('Lumber_Grade',on_delete=models.CASCADE)
    breadth = models.DecimalField(max_digits=5, decimal_places=2)
    depth = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.wood_choice


# class Lumber(models.Model):
#    """Used to select different,
#        lumber types: glulam, dimensional, uncut (?),
#        lumber size: Different tables for (2-4") and (5"x5" or larger) and
#        Grades"""
#    lumber_type = "Nothing Yet."
#    lumber_grade = "Nothing Yet."
#    lumber_size = "Nothing Yet."
#    def __str__(self):
#        return self.lumber_type


class Lumber_Type(models.Model):
    """Used to select different lumber types: glulam, dimensional, uncut (?)"""

    lumber_type = "Nothing Yet."
    pass

    def __str__(self):
        return self.lumber_type


class Lumber_Grade(models.Model):
    """Used to select different Grades"""

    lumber_grade = "Nothing Yet."
    pass

    def __str__(self):
        return self.lumber_grade


class Lumber_Size(models.Model):
    """Used to select different lumber size: Different tables for (2-4") and (5"x5" or larger)"""

    lumber_size = "Nothing Yet."
    pass

    def __str__(self):
        return self.lumber_size
