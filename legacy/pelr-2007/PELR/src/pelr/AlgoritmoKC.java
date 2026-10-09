/*
 * AlgoritmoKC.java
 *
 * Created on 31 de enero de 2007, 15:03
 *
 */

package pelr;

import estdatos.*;
import java.util.Vector;

/**
 *
 * @author Daniel Moral García
 */
public class AlgoritmoKC {
    
    /** Creates a new instance of AlgoritmoKC */
    //public AlgoritmoKC() {
    //}
    
    /**
     *  Funcion que nos devuelve cierto si dos estados se deben unir y falso en
     *   caso contrario.
     *@param primero Nombre del primer estado a comprobar
     *@param segundo Nombre del segundo estado a comprobar
     *@param orden Numero de caracteres que tienen que ser comunes en ambos estados
     *@return Cierto si ambos estados deben unirse, falso en caso contrario.
     */
    private static boolean seUne(String primero, String segundo, int orden) {
        String p;
        String s;
        if (primero.length()>orden) p = primero.substring(primero.length()-orden,primero.length());
        else p = primero;
        if (segundo.length()>orden) s = segundo.substring(segundo.length()-orden,segundo.length());
        else s = segundo;
        
        return p.equals(s);
    }
    
    /** 
     *  Funcion principal del algoritmo. Necesita el arbol de prefijos, tipo de
     *   Algoritmo a utilizar (normal, incremental o con muestra negativa), un
     *   valor K y la muestra negativa.
     *@param arbol Autamata sobre el que aplicaremos el algoritmo KC
     *@param alg Indice del algoritmo (3-KC; 4-KC Imcremental; 5-KC con negativos)
     *@param valK Valor de K para el algoritmo KC
     *@param mnegativa Muestra negativa (usada en KC con negativos)
     *@return Devuelve un automata que contiene el resultado de aplicar el algoritmo KC
    */
    public static Automata ejecutar(Automata arbol, int alg, int valK, Vector mnegativa) {
        Automata b = new Automata();
        int primero,segundo;
        // Booleanos para saber si un determinado estado ya ha sido tratado.
        boolean cond[] = new boolean[arbol.obtenerNumeroEstados()];
        boolean anad[] = new boolean[arbol.obtenerNumeroEstados()];
        boolean pertenece = false;
        Vector aux,aux2 = new Vector();
        Estado temporal2;
        
        b.putAlfEntrada(arbol.getAlfEntrada());
        b.putSimbolos(arbol.getSimbolos());
        Estado temporal = arbol.obtenerEstado(0);
        if (b.addEstado(new Estado(temporal))) {
            for (int i=0; i<arbol.obtenerNumeroEstados(); i++) {
                primero = b.buscarEstado(arbol.obtenerEstado(i));
                for (int j=i; j<arbol.obtenerNumeroEstados(); j++) {
                    if (i!=j) {
                        if (anad[j] == false) {
                            temporal = arbol.obtenerEstado(j);
                            if (b.addEstado(new Estado(temporal))) {
                                anad[j]=true;
                            }
                        }
                        if (seUne(arbol.obtenerEstado(i).getEstado(0),arbol.obtenerEstado(j).getEstado(0),valK)&&cond[j]==false) {
                            //System.out.println("KC incremental El estado "+arbol.obtenerEstado(i).getEstado(0)+" y el estado "+arbol.obtenerEstado(j).getEstado(0)+" se juntan");
                            segundo = b.buscarEstado(arbol.obtenerEstado(j));
                            b.uneEstados(primero,segundo);
                            cond[j] = true;
                        }
                    }
                }
            } //Fin del primer FOR
        }

        // Ahora generamos las transiciones para los grupos de estados
        for (int i=0; i<arbol.obtenerNumeroEstados(); i++) {
            temporal = (Estado)arbol.obtenerEstado(i);
            for (int j=0; j<arbol.getSimbolos().size(); j++) {
                try {
                    aux = arbol.getTransicion(i,j);
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
                catch (Exception err) {}
            }
        }
        // Retornamos el automata resultado.
        return b;
    }
    
}
