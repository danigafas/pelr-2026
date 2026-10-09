/*
 * AlgoritmoIM1.java
 *
 * Created on 31 de enero de 2007, 14:58
 *
 */

package pelr;

import java.util.Vector;
import estdatos.Automata;
import estdatos.Estado;

/**
 *
 * @author Daniel Moral García
 */
public class AlgoritmoIM1 {
     
    /** Constructor por defecto */
    //public AlgoritmoIM1() {
    //}
    
    /**
     *  Funcion T para la muestra positiva. 
     *  Necesita un vector delta con las transiciones del automata, un estado 
     *   (para el que se quiere calcular) y el orden de profundidad del 
     *   algoritmo.
     *@param a Automata aceptor de prefijos para calcular las T's
     *@param e Estado para el cual se quiere calcular T
     *@param orden Profundidad del algoritmo
     *@return Devuelve un Vector con el resultado del algoritmo. Cada posicion del vector es un estado.
    */
    public static Vector Tspos(Automata a, Estado e, int orden) {
        Vector result = new Vector();
        Vector resTemp = new Vector();
        Estado temporal = new Estado();
        Vector trTMP = new Vector();
             
        //Caso base: si es de orden 1
        if (orden==1) {
            for (int i=0; i<a.getSimbolos().size(); i++) {
                try {
                    trTMP = a.getTransicion(a.obtenerIndiceEstado(e),i);
                    temporal = (Estado)trTMP.elementAt(0);
                    if (temporal.getTipoEstado()=="FINAL")
                        result.addElement(a.getSimbolos().elementAt(i));
                }
                catch (Exception error) {}
            }
            if (((e.getTipoEstado()=="FINAL")||(e.getTipoEstado()=="INICIAL/FINAL")))
                result.addElement("%");
            return result;
        }
        //Si es de orden superior a 1, recursion.
        else if (orden>1) {
            //Para cada simbolo del alfabeto
            for (int i=0; i<a.getSimbolos().size(); i++) {
                try {
                    //La recursion: llamamos a la funcion pasandole el automata, la transicion
                    //para el simbolo actual, y el orden menos 1.
                    trTMP = a.getTransicion(a.obtenerIndiceEstado(e),i);
                    result.addAll(Tspos(a,(Estado)trTMP.elementAt(0),orden-1));
                    for (int j=0; j<result.size(); j++) {
                        String aux = result.elementAt(j).toString();
                        if ((aux!="%")&&(aux.length()<orden)) {
                            String tmp = a.getSimbolos().elementAt(i).toString();
                            String tmp2 = result.elementAt(j).toString();
                            aux = tmp.concat(tmp2);
                            if (!result.contains(aux)) result.setElementAt(aux,j);
                        }
                    }
                }
                catch (Exception error) {}
            }
        }
        if (orden>0) resTemp.addAll(Tspos(a,e,orden-1));
        for (int i=0; i<resTemp.size(); i++) {
            if (!result.contains(resTemp.elementAt(i))) result.addElement(resTemp.elementAt(i));
        }
        resTemp.removeAllElements();
        for (int i=0; i<result.size(); i++) {
            try {
                temporal = a.getTransicionEstrella(a.obtenerIndiceEstado(e),result.elementAt(i).toString());
                resTemp.addElement(result.elementAt(i));
            }
            catch (Exception err) {}
        }
        if (((e.getTipoEstado()=="FINAL")||(e.getTipoEstado()=="INICIAL/FINAL")))
            resTemp.addElement("%");
        return resTemp;
    }
    
    /**
     * Funcion que calcula los valores de la funcion T para todos los estados del
     *  automata. Necesita tambien el orden de profundidad (valor K).
     * Devuelve un vector con los valores de la funcion para cada estado.
     *@param a Automata para calcular las T's (arbol de prefijos)
     *@param k Parametro K del algoritmo que calculas las T's
     *@return Devuelve un Vector que contiene las T's de todos los estados.
    */
    private static Vector calculaTs(Automata a, int k) {
        Vector vtemp,result = new Vector();
        Estado temp = new Estado();
        
        for (int i=0; i<a.obtenerNumeroEstados(); i++) {
            temp = (Estado)a.obtenerEstado(i);
            vtemp = (Vector)Tspos(a,temp,k);
            result.addElement((Vector)vtemp.clone());
        }
        return result;
    }
    
    /**
     *  Funcion que calcula la interseccion de dos vectores dados. Devuelve otro vector.
     *@param v1 Primer vector
     *@param v2 Segundo vector
     *@return Un vector con la interseccion de los vectores pasados como parametro
    */
    public static Vector interseccion(Vector v1, Vector v2) {
        Vector result = new Vector();
        for (int i=0; i<v1.size(); i++) {
            if (v2.contains(v1.elementAt(i))) result.addElement(v1.elementAt(i));
        }
        return result;
    }
    
    /**
     *  Funcion que ejecuta el algoritmo con el heuristico de los k-sufijos
     *  Necesita un automata.
     *@param vecTes Vector que contiene las T's del arbol
     *@param estado1 Indice del primer estado a comprobar
     *@param estado2 Indice del segundo estado
     *@return Cierto si los dos estado deben unirse, falso en caso contrario.
    */
    public static boolean conKSufijos(Vector vecTes, int estado1, int estado2) {
        return vecTes.elementAt(estado1).equals(vecTes.elementAt(estado2));
    }
    
    /**
     *  Funcion que ejecuta el algoritmo con el heuristico de Levine
     *  Necesita un automata.
     *@param automata Automata al que se va a aplicar Levine
     *@param u Indice del primer estado
     *@param v Indice del segundo estado.
     *@param s Parametro S del heuristico de Levine
     *@return Cierto si los dos estado deben unirse, falso en caso contrario.
    */
    public static boolean conLevine(Automata automata, int u, int v, double s) {
        double max = -1;
        double stren = -1;
        Vector intersec = new Vector();
        Vector aux1 = new Vector();
        Vector aux2 = new Vector();
        
        // Esto es para saber hasta que orden hay que calcular las T's
        int longMax = automata.obtenerEstado(0).getEstado(0).length();
        for (int i=1; i<automata.obtenerNumeroEstados(); i++)
            if ( automata.obtenerEstado(i).getEstado(0).length() > longMax )
                longMax = automata.obtenerEstado(i).getEstado(0).length();
        
        for (int i=0; i<=longMax; i++) {
            aux1 = Tspos(automata,automata.obtenerEstado(u),i);
            aux2 = Tspos(automata,automata.obtenerEstado(v),i);
            intersec = interseccion(aux1,aux2);
            float denominador = aux1.size()+aux2.size();
            if (denominador!=0) stren = ((2*intersec.size())/denominador);
            else stren=0;
            if (stren>max) max=stren;
        }
        if (max>=s) return true;
        else return false;
    }
    
    /**
     *  Funcion principal de algoritmo. Necesita un automata, el indice del 
     *      heuristico a utilizar y los parametros K y S.
     *  No devuelve nada. Los resultados se muestran por pantalla.
     *@param automata Automata sobre el que se aplicara IM1
     *@param alg Indice del algoritmo (0-KSufijos; 1-Levine; 2-Miclet)
     *@param vk Valor de K (usado en KSufijos)
     *@param vs Valor de S (usado por Levine y Miclet)
     *@return Devuelve un automata que contiene el resultado de aplicar el algoritmo IM1
    */
    public static Automata ejecutar(Automata automata, int alg, int vk, double vs) {
        Vector vecTes = new Vector();
        Vector aux,aux2 = new Vector();
        Automata b = new Automata();
        Estado temporal2;
        int primero,segundo;
        boolean pertenece = false;
        
        vecTes = calculaTs(automata,vk);
        // Booleanos para saber si un determinado estado ya ha sido tratado
        boolean cond[] = new boolean[vecTes.size()];
        boolean anad[] = new boolean[automata.obtenerNumeroEstados()];
        
        b.putAlfEntrada(automata.getAlfEntrada());
        b.putSimbolos(automata.getSimbolos());
        Estado temporal = automata.obtenerEstado(0);
        
        if (b.addEstado(new Estado(temporal))) {
            for (int i=0; i<automata.obtenerNumeroEstados(); i++) {
                primero = b.buscarEstado(automata.obtenerEstado(i));
                for (int j=i; j<automata.obtenerNumeroEstados(); j++) {
                    if (i!=j) {
                        if (anad[j] == false) {
                            temporal = automata.obtenerEstado(j);
                            if (b.addEstado(new Estado(temporal))) {
                                anad[j]=true;
                            }
                        }
                        switch (alg) {
                            case 0: //Algoritmo IM1 con k-sufijos
                                if (conKSufijos(vecTes,i,j)&&cond[j]==false) {
                                    //System.out.println("KSufijos El estado "+automata.obtenerEstado(i).getEstado(0)+" y el estado "+automata.obtenerEstado(j).getEstado(0)+" se juntan");
                                    segundo = b.buscarEstado(automata.obtenerEstado(j));
                                    b.uneEstados(primero,segundo);
                                    cond[j] = true;
                                }
                                break; 
                            case 1: //Algoritmo IM1 con Levine
                                if (conLevine(automata,i,j,vs)&&cond[j]==false) {
                                    //System.out.println("Levine El estado "+b.obtenerEstado(i).getEstado(0)+" y el estado "+b.obtenerEstado(j).getEstado(0)+" se juntan");
                                    segundo = b.buscarEstado(automata.obtenerEstado(j));
                                    b.uneEstados(primero,segundo);
                                    cond[j] = true;
                                }                            
                                break; 
                            case 2: //Algoritmo IM1 con Miclet
                                // Miclet y Levine son iguales. La única diferencia es el valor
                                // vs que se le pase a la funcion.
                                if (conLevine(automata,i,j,vs)&&cond[j]==false) {
                                    //System.out.println("Miclet El estado "+b.obtenerEstado(i).getEstado(0)+" y el estado "+b.obtenerEstado(j).getEstado(0)+" se juntan");
                                    segundo = b.buscarEstado(automata.obtenerEstado(j));
                                    b.uneEstados(primero,segundo);
                                    cond[j] = true;
                                } 
                                break; 
                        }
                    }
                }
            }
        }
        
        // Ahora generamos las transiciones para los grupos de estados
        for (int i=0; i<automata.obtenerNumeroEstados(); i++) {
            temporal = (Estado)automata.obtenerEstado(i);
            for (int j=0; j<automata.getSimbolos().size(); j++) {
                try {
                    aux = automata.getTransicion(i,j);
                    primero = b.buscarEstado(temporal);
                    try {
                        aux2 = b.getTransicion(primero,j);
                        for (int s=0; s<aux2.size(); s++) {
                            temporal2 = (Estado)aux2.elementAt(s);
                            if (temporal2.comparaEstado(b.obtenerEstado(b.buscarEstado((Estado)aux.elementAt(0))))) {
                                pertenece=true;
                            }
                        }
                        if (!pertenece) b.addTransicion(primero,j,b.obtenerEstado(b.buscarEstado((Estado)aux.elementAt(0))));
                    }
                    catch (Exception err) {
                        b.addTransicion(primero,j,b.obtenerEstado(b.buscarEstado((Estado)aux.elementAt(0))));
                    }
                }
                catch (Exception err) {
                }
            }
        }
        // Devolvemos el automata resultado
        return b;
    }
}
