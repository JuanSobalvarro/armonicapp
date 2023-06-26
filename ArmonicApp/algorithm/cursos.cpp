#include <iostream>
#include <cstdlib>
using namespace std;

int main() {
	string cursos[4]; int cred[4]; double note[4]; bool calif[4]; double total[4] = {0,0,0,0};
	
	for(int i=0; i!=4; i++) {
		cout << "Ingrese la informacion del curso " << i+1 << endl;
		cout << "Nombre: "; cin >> cursos[i];
		cout << "Creditos: "; cin >> cred[i];
		cout << "Calificacion(0-100): "; cin >> note[i];
		if(note[i] >= 70) {
			calif[i] = true;
		}
		else {
			calif[i] = false;
		}
	}
	
	cout << "|	Curso	|	Creditos	|	Nota	|	Clasificacion			|\n";
	for(int i=0; i != 4; i++) {
		cout << "|	" << cursos[i] << "	|	" << cred[i] << "		|	" << note[i] << "	|		" << calif[i] << "			|\n";
		total[0] += cred[i];
		total[1] += note[i];
		if(calif[i]) {
			total[2] += 1;
		}
		else {
			total[3] += 1;
		}
	}
	total[1] = total[1]/4;
	
	cout << "|	Total	|	" << total[0] << "		|	" << total[1] << "	|	" << total[2] << " aprobadas y " << total[3] << " reprobadas	|";
	
	return 0;
}

