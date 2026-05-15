import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# JSON data provided
data = {
	"table": "clips",
	"rows":
	[
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 0,
			"primary_category": "Insecto",
			"promedio_clips_hora": 66.8,
			"pct_composicion_hora": 61.54
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 0,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 32.98,
			"pct_composicion_hora": 30.39
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 0,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 7.48,
			"pct_composicion_hora": 6.89
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 0,
			"primary_category": "Ave",
			"promedio_clips_hora": 1.18,
			"pct_composicion_hora": 1.09
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 0,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.1,
			"pct_composicion_hora": 0.09
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 1,
			"primary_category": "Insecto",
			"promedio_clips_hora": 59.84,
			"pct_composicion_hora": 63.67
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 1,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 28.02,
			"pct_composicion_hora": 29.81
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 1,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 3.98,
			"pct_composicion_hora": 4.23
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 1,
			"primary_category": "Ave",
			"promedio_clips_hora": 1.1,
			"pct_composicion_hora": 1.17
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 1,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 1.04,
			"pct_composicion_hora": 1.11
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 2,
			"primary_category": "Insecto",
			"promedio_clips_hora": 59.12,
			"pct_composicion_hora": 67.47
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 2,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 24.56,
			"pct_composicion_hora": 28.03
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 2,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 2.98,
			"pct_composicion_hora": 3.4
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 2,
			"primary_category": "Ave",
			"promedio_clips_hora": 0.86,
			"pct_composicion_hora": 0.98
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 2,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.1,
			"pct_composicion_hora": 0.11
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 3,
			"primary_category": "Insecto",
			"promedio_clips_hora": 58.32,
			"pct_composicion_hora": 69.66
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 3,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 20.1,
			"pct_composicion_hora": 24.01
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 3,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 4.16,
			"pct_composicion_hora": 4.97
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 3,
			"primary_category": "Ave",
			"promedio_clips_hora": 1.0,
			"pct_composicion_hora": 1.19
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 3,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.14,
			"pct_composicion_hora": 0.17
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 4,
			"primary_category": "Insecto",
			"promedio_clips_hora": 57.16,
			"pct_composicion_hora": 67.6
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 4,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 19.46,
			"pct_composicion_hora": 23.01
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 4,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 4.46,
			"pct_composicion_hora": 5.27
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 4,
			"primary_category": "Ave",
			"promedio_clips_hora": 3.24,
			"pct_composicion_hora": 3.83
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 4,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.24,
			"pct_composicion_hora": 0.28
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 5,
			"primary_category": "Insecto",
			"promedio_clips_hora": 60.56,
			"pct_composicion_hora": 67.76
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 5,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 15.82,
			"pct_composicion_hora": 17.7
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 5,
			"primary_category": "Ave",
			"promedio_clips_hora": 7.82,
			"pct_composicion_hora": 8.75
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 5,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 5.02,
			"pct_composicion_hora": 5.62
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 5,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.16,
			"pct_composicion_hora": 0.18
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 6,
			"primary_category": "Insecto",
			"promedio_clips_hora": 54.42,
			"pct_composicion_hora": 53.99
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 6,
			"primary_category": "Ave",
			"promedio_clips_hora": 36.44,
			"pct_composicion_hora": 36.15
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 6,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 8.34,
			"pct_composicion_hora": 8.27
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 6,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 1.24,
			"pct_composicion_hora": 1.23
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 6,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 0.36,
			"pct_composicion_hora": 0.36
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 7,
			"primary_category": "Insecto",
			"promedio_clips_hora": 58.72,
			"pct_composicion_hora": 58.24
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 7,
			"primary_category": "Ave",
			"promedio_clips_hora": 25.28,
			"pct_composicion_hora": 25.07
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 7,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 15.46,
			"pct_composicion_hora": 15.33
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 7,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.94,
			"pct_composicion_hora": 0.93
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 7,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 0.42,
			"pct_composicion_hora": 0.42
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 8,
			"primary_category": "Insecto",
			"promedio_clips_hora": 54.88,
			"pct_composicion_hora": 57.49
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 8,
			"primary_category": "Ave",
			"promedio_clips_hora": 26.76,
			"pct_composicion_hora": 28.03
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 8,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 12.14,
			"pct_composicion_hora": 12.72
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 8,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 1.34,
			"pct_composicion_hora": 1.4
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 8,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 0.34,
			"pct_composicion_hora": 0.36
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 9,
			"primary_category": "Insecto",
			"promedio_clips_hora": 37.46,
			"pct_composicion_hora": 45.74
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 9,
			"primary_category": "Ave",
			"promedio_clips_hora": 28.8,
			"pct_composicion_hora": 35.16
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 9,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 14.36,
			"pct_composicion_hora": 17.53
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 9,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 1.1,
			"pct_composicion_hora": 1.34
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 9,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 0.18,
			"pct_composicion_hora": 0.22
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 10,
			"primary_category": "Insecto",
			"promedio_clips_hora": 49.46,
			"pct_composicion_hora": 47.01
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 10,
			"primary_category": "Ave",
			"promedio_clips_hora": 37.54,
			"pct_composicion_hora": 35.68
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 10,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 17.02,
			"pct_composicion_hora": 16.18
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 10,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.88,
			"pct_composicion_hora": 0.84
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 10,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 0.32,
			"pct_composicion_hora": 0.3
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 11,
			"primary_category": "Insecto",
			"promedio_clips_hora": 53.48,
			"pct_composicion_hora": 53.22
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 11,
			"primary_category": "Ave",
			"promedio_clips_hora": 27.62,
			"pct_composicion_hora": 27.49
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 11,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 18.26,
			"pct_composicion_hora": 18.17
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 11,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.86,
			"pct_composicion_hora": 0.86
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 11,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 0.26,
			"pct_composicion_hora": 0.26
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 12,
			"primary_category": "Insecto",
			"promedio_clips_hora": 41.34,
			"pct_composicion_hora": 46.69
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 12,
			"primary_category": "Ave",
			"promedio_clips_hora": 25.9,
			"pct_composicion_hora": 29.25
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 12,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 18.78,
			"pct_composicion_hora": 21.21
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 12,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 2.16,
			"pct_composicion_hora": 2.44
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 12,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 0.36,
			"pct_composicion_hora": 0.41
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 13,
			"primary_category": "Insecto",
			"promedio_clips_hora": 50.72,
			"pct_composicion_hora": 59.21
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 13,
			"primary_category": "Ave",
			"promedio_clips_hora": 19.0,
			"pct_composicion_hora": 22.18
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 13,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 14.88,
			"pct_composicion_hora": 17.37
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 13,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.7,
			"pct_composicion_hora": 0.82
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 13,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 0.36,
			"pct_composicion_hora": 0.42
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 14,
			"primary_category": "Insecto",
			"promedio_clips_hora": 51.76,
			"pct_composicion_hora": 53.62
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 14,
			"primary_category": "Ave",
			"promedio_clips_hora": 22.5,
			"pct_composicion_hora": 23.31
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 14,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 20.3,
			"pct_composicion_hora": 21.03
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 14,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 1.5,
			"pct_composicion_hora": 1.55
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 14,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 0.48,
			"pct_composicion_hora": 0.5
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 15,
			"primary_category": "Insecto",
			"promedio_clips_hora": 68.62,
			"pct_composicion_hora": 66.08
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 15,
			"primary_category": "Ave",
			"promedio_clips_hora": 17.4,
			"pct_composicion_hora": 16.76
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 15,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 15.88,
			"pct_composicion_hora": 15.29
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 15,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 1.3,
			"pct_composicion_hora": 1.25
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 15,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 0.64,
			"pct_composicion_hora": 0.62
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 16,
			"primary_category": "Insecto",
			"promedio_clips_hora": 74.34,
			"pct_composicion_hora": 65.15
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 16,
			"primary_category": "Ave",
			"promedio_clips_hora": 20.84,
			"pct_composicion_hora": 18.26
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 16,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 15.92,
			"pct_composicion_hora": 13.95
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 16,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 2.78,
			"pct_composicion_hora": 2.44
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 16,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.22,
			"pct_composicion_hora": 0.19
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 17,
			"primary_category": "Insecto",
			"promedio_clips_hora": 77.7,
			"pct_composicion_hora": 61.13
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 17,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 27.22,
			"pct_composicion_hora": 21.42
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 17,
			"primary_category": "Ave",
			"promedio_clips_hora": 19.18,
			"pct_composicion_hora": 15.09
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 17,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 2.76,
			"pct_composicion_hora": 2.17
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 17,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.24,
			"pct_composicion_hora": 0.19
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 18,
			"primary_category": "Insecto",
			"promedio_clips_hora": 93.44,
			"pct_composicion_hora": 68.44
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 18,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 31.26,
			"pct_composicion_hora": 22.9
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 18,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 6.06,
			"pct_composicion_hora": 4.44
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 18,
			"primary_category": "Ave",
			"promedio_clips_hora": 5.7,
			"pct_composicion_hora": 4.18
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 18,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.06,
			"pct_composicion_hora": 0.04
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 19,
			"primary_category": "Insecto",
			"promedio_clips_hora": 100.62,
			"pct_composicion_hora": 72.23
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 19,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 35.64,
			"pct_composicion_hora": 25.59
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 19,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 1.88,
			"pct_composicion_hora": 1.35
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 19,
			"primary_category": "Ave",
			"promedio_clips_hora": 1.14,
			"pct_composicion_hora": 0.82
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 19,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.02,
			"pct_composicion_hora": 0.01
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 20,
			"primary_category": "Insecto",
			"promedio_clips_hora": 82.24,
			"pct_composicion_hora": 61.31
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 20,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 42.98,
			"pct_composicion_hora": 32.04
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 20,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 7.58,
			"pct_composicion_hora": 5.65
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 20,
			"primary_category": "Ave",
			"promedio_clips_hora": 1.06,
			"pct_composicion_hora": 0.79
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 20,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.28,
			"pct_composicion_hora": 0.21
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 21,
			"primary_category": "Insecto",
			"promedio_clips_hora": 74.34,
			"pct_composicion_hora": 56.28
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 21,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 44.58,
			"pct_composicion_hora": 33.75
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 21,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 11.54,
			"pct_composicion_hora": 8.74
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 21,
			"primary_category": "Ave",
			"promedio_clips_hora": 1.2,
			"pct_composicion_hora": 0.91
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 21,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.42,
			"pct_composicion_hora": 0.32
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 22,
			"primary_category": "Insecto",
			"promedio_clips_hora": 65.56,
			"pct_composicion_hora": 53.37
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 22,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 40.16,
			"pct_composicion_hora": 32.69
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 22,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 15.54,
			"pct_composicion_hora": 12.65
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 22,
			"primary_category": "Ave",
			"promedio_clips_hora": 1.44,
			"pct_composicion_hora": 1.17
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 22,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.14,
			"pct_composicion_hora": 0.11
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 23,
			"primary_category": "Insecto",
			"promedio_clips_hora": 63.5,
			"pct_composicion_hora": 57.02
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 23,
			"primary_category": "Antropogénico",
			"promedio_clips_hora": 36.18,
			"pct_composicion_hora": 32.49
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 23,
			"primary_category": "Anfibio",
			"promedio_clips_hora": 9.96,
			"pct_composicion_hora": 8.94
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 23,
			"primary_category": "Ave",
			"promedio_clips_hora": 1.52,
			"pct_composicion_hora": 1.36
		},
		{
			"localidad": "12 DE ABRIL",
			"hora_dia": 23,
			"primary_category": "Mamífero",
			"promedio_clips_hora": 0.2,
			"pct_composicion_hora": 0.18
		}
	]
}

# 1. Preparar el DataFrame
df = pd.DataFrame(data["rows"])

# Mapeo de traducción (Español a Inglés)
translation = {
    "Antropogénico": "Anthropogenic",
    "Mamífero": "Mammal",
    "Anfibio": "Amphibian",
    "Insecto": "Insect",
    "Ave": "Bird"
}
df['primary_category'] = df['primary_category'].map(translation)

# 2. Reestructurar datos para el gráfico de área (stackplot)
# El orden de las categorías define las capas (de abajo hacia arriba)
pivot_df = df.pivot(index='hora_dia', columns='primary_category', values='promedio_clips_hora')
categories_order = ["Anthropogenic", "Mammal", "Amphibian", "Insect", "Bird"]
pivot_df = pivot_df[categories_order]

# 3. Configuración del gráfico
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid", rc={"grid.alpha": 0.3})

# Colores que replican los de la foto (Rojizo, Naranja, Azul, Amarillo, Verde)
colors = ["#E67161", "#E69C55", "#63B0E6", "#F2D04E", "#61D28F"]

# Crear el Stackplot (Gráfico de área apilada)
plt.stackplot(pivot_df.index, pivot_df.T, labels=pivot_df.columns, colors=colors)

# Títulos y etiquetas en Inglés
plt.title('Average Activity 24h - Location 12 DE ABRIL', fontsize=14, fontweight='bold')
plt.xlabel('Hour of the day', fontsize=11)
plt.ylabel('Average Detected Clips', fontsize=11)

# Eje X: Mostrar todas las horas de 0 a 23
plt.xticks(range(0, 24))
plt.xlim(0, 23)

# Leyenda (ubicada arriba a la izquierda como en la foto)
plt.legend(title='Category', loc='upper left', frameon=True, fontsize='small')

plt.tight_layout()

# 4. Guardar archivo
output_file = "activity_area_chart.png"
plt.savefig(output_file, dpi=300)
plt.show()

print(f"Plot saved successfully as {output_file}")