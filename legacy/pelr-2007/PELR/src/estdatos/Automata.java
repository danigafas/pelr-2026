/*
 * Automata.java
 *
 * Created on 15 de diciembre de 2006, 17:25
 *
 *
 */

package estdatos;
import java.util.Vector;
import java.io.Serializable;
import java.io.*;
import javax.swing.JOptionPane;

/**
 *
 * @author  Daniel Moral García
 */

public class Automata implements Serializable {
    
    private Vector vEstados; //Vector de estados
    private Vector alfabetoEntrada; //alfabeto de entrada del automata
    private Vector alfabetoSalida; //Alfabeto de salida del automata
    private Vector delta; //Funcion delta del automata
    private String tipo; //Tipo de automata. AFD, AFND, MOORE, MEALY, etc
    private Vector fSalida; //Funcion de salida(Moore y Mealy)
    private Vector simbolos; // Vector con los simbolos del alfabeto.
    
    /**
     *  Constructor por defecto de un automata. No necesita nada.
     *@return No devuelve nada
    */
    public Automata() {
        vEstados = new Vector();
        alfabetoEntrada = new Vector();
        alfabetoSalida = new Vector();
        delta = new Vector();
        tipo = "";
        fSalida = new Vector();
        simbolos = new Vector();
    }
    
    /**
     *  Constructor de un automata al que se le pasa un vector de estados,
     *  un alfabeto de entrada y una funcion delta.
     *@param ve Un vector de estados
     *@param ae Un vector con el alfabeto de entrada
     *@param d Un vector con la funcion delta
     *@param simb Un vector con los simbolos del alfabeto
     *@return No devuelve nada
    */
    public Automata (Vector ve, Vector ae, Vector d, Vector simb) {
        vEstados = (Vector)ve.clone();
        alfabetoEntrada = (Vector)ae.clone();
        delta = (Vector)d.clone();
        simbolos = (Vector)simb.clone();
    }
    
    /**
     *  Constructor de copia de la clase automata. Necesita un automata.
     *@param a Un Automata
     *@return No devuelve nada
    */
    public Automata (Automata a) {
        vEstados = (Vector)a.vEstados.clone();
        alfabetoEntrada = (Vector)a.alfabetoEntrada.clone();
        alfabetoSalida = (Vector)a.alfabetoSalida.clone();
        delta = (Vector)a.delta.clone();
        fSalida = (Vector)a.fSalida.clone();
        simbolos = (Vector)a.simbolos.clone();
    }
    
    /**
     *  Funcion que modifica el vector de estados del automata
     * @param ve Un vector con la lista de estados
     * @return No devuelve nada
    */
    public void putVectorEstados(Vector ve) {
        vEstados = (Vector)ve.clone();
    }
    
    /**
     *  Funcion que modifica el alfabeto de entrada del automata.
     *@param ae Un vector con el alfabeto de entrada
     *@return No devuelve nada
    */       
    public void putAlfEntrada(Vector ae) {
        alfabetoEntrada = (Vector)ae.clone();
    }
    
    /**
     *  Funcion que modifica el alfabeto de salida del automata.
     *@param as Un vector con el alfabeto de salida
     *@return No devuelve nada
    */
    public void putAlfSalida(String[] as) {
        alfabetoSalida = (Vector)as.clone();
    }
    
    /**
     *  Funcion que modifica la funcion delta del automata.
     * @param d Un vector con la función delta
     *@return No devuelve nada
    */
    public void putDelta(Vector d) {
        delta = (Vector)d.clone();
    }
    
    /**
     *  Funcion que modifica la funcion de salida el automata.
     * @param fs Un vector con la funcion de salida
     *@return No devuelve nada
    */
    public void putFSalida(Vector fs) {
        fSalida = (Vector)fs.clone();
    }
    
    /**
     *  Funcion que modifica la tabla de simbolos del alfabeto
     *@param s un vector que contenga los simbolos del alfabeto
     *@return No devuelve nada
    */
    public void putSimbolos(Vector s) {
        simbolos = (Vector)s.clone();
    }
    
    /**
     *  Funcion que añade un simbolo al alfabeto del automata
     *@param s Un simbolo del alfabeto
     *@return No devuelve nada
     */
    public void addSimbolo(String s) {
        if (!simbolos.contains(s)) simbolos.addElement(s);
    }
    
    /**
     * Funcion que elimina un simbolo del alfabeto
     *@param s Un simbolo del alfabeto
     *@return No devuelve nada
     */
    public void delSimbolo(String s) {
        if (simbolos.contains(s)) 
            simbolos.removeElement(s);
    }
    
    /**
     *  Funcion que devuelve el vector de estados del automata
     *@return Vector
     */
    public Vector getVectorEstados() {
        return vEstados;
    }
    
    /**
     *  Funcion que devuelve el alfabeto de entrada del automata
     *@return Vector
     */
    public Vector getAlfEntrada() {
        return alfabetoEntrada;
    }
    
    /**
     *  Funcion que devuelve el alfabeto de salida del automata
     *@return Vector
     */
    public Vector getAlfSalida() {
        return alfabetoSalida;
    }
    
    /**
     * Retorna la funcion delta asociada al automata.
     *@return Vector
     */
    public Vector getDelta() {
        return delta;
    }
    
    /**
     * Devuelve la funcion de salida.
     *@return Vector
     */
    public Vector getFSalida() {
        return fSalida;
    }
    
    /**
     * Devuelve la tabla de simbolos
     *@return Vector
     */
    public Vector getSimbolos() {
        return simbolos;
    }
    
    /**
     *  Funcion que añade un estado al vector de estados.
     *@param e Un estado para añadir
     *@return Cierto si se pudo añadir el estado y falso en caso contrario.
    */
    public boolean addEstado(Estado e) {
        if (this.buscarEstado(e)==-1) {
            vEstados.addElement(e);
            return true;
        }
        return false;
    }
    
    /**
     *  Añade un estado generando las transiciones (Arbol de prefijos para IM1 
     *   y KC)
     *@param e Un estado para añadir
     *@return Cierto si se pudo añadir el estado con la transicion. Falso en caso contrario
     */
    public boolean addEstadoTransicion(Estado e) {
        if (this.addEstado(e)) {
            //Ahora le añadimos la transicion correspondiente
            String simbActual,cadActual,cadena;
            cadena = e.getEstado(0);
            cadActual = cadena;
            Estado etemp = new Estado("%");
            for (int i=0; i<cadena.length(); i++) {
                simbActual = cadActual.substring(0,1);
                if (simbolos.indexOf(simbActual) == -1) simbolos.addElement(simbActual);
                cadActual = cadActual.substring(1);
                try {
                    etemp = (Estado)getTransicion(obtenerIndiceEstado(etemp),simbolos.indexOf(simbActual)).elementAt(0);
                }
                catch (Exception err) {
                    this.addTransicion(this.buscarEstado(etemp),simbolos.indexOf(simbActual),e);
                }
            }
            return true;
        }
        return false;
    }
    
    /**
     *  Borra un estado
     *@param e Un estado para borrar
     *@return No devuelve nada
     */
    public void delEstado(Estado e) {
        int i = this.obtenerIndiceEstado(e);
        if (i!=-1) vEstados.removeElementAt(i);
    }
    
    /**
     * Devuelve el nombre del estado de la posicion indicada.
     *@param indice El indice de un estado
     *@return Devuelve el estado asociado a ese indice.
     */
    public Estado obtenerEstado(int indice) {
        return (Estado)vEstados.elementAt(indice);
    }
    
    /**
     *   Funcion que nos devuelve el indice de un estado dado. Si no se
     *    encuentra el estado devuelve -1.
     *@param e El estado del cual queremos saber el indice
     *@return El indice del estado. Devuelve -1 si no se encuentra
    */
    public int obtenerIndiceEstado(Estado e) {
        Estado eTMP;
        for (int i=0; i<vEstados.size(); i++) {
            eTMP = (Estado)vEstados.elementAt(i);
            if (eTMP.comparaEstado(e)) return i;
        }
        return -1;
    }
    
    /**
     *  Funcion que nos dice en que grupo de estados se encuentra un determinado
     *   estado. Devuelve el indice del estado si lo encuentra o -1 en caso 
     *   contrario.
     *@param e El estado del cual queremos saber el indice
     *@return El indice del estado en que se encuentra un determinado estado. Devuelve -1 si no se encuentra
     */
    public int buscarEstado(Estado e) {
        Estado tmp;
        for (int i=0; i<vEstados.size(); i++) {
            tmp = (Estado)vEstados.elementAt(i);
            for (int j=0; j<tmp.getNumEstados(); j++)
                if (e.getEstado(0).equals(tmp.getEstado(j))) return i;
        }
        return -1;
    }
    
    /**
     * Devuelve el numero de estados del automata
     *@return Numero de estados del automata
     */
    public int obtenerNumeroEstados() {
        return vEstados.size();
    }
    
    /**
     *  Funcion que elimina todas las transiciones del automata
     *@return No devuelve nada
     */
    public void limpiaTransiciones() {
        delta.removeAllElements();
    }
    
    /**
     *  Añade una nueva transicion al automata. Necesita el identificador del
     *   estado y del simbolo, asi como un estado destino (donde se llega con
     *   la transicion).
     *@param estado Indice del estado origen
     *@param simbolo Simbolo con el que se añadira la transicion
     *@param destino Estado destino
     *@return No devuelve nada
    */
    public void addTransicion(int estado, int simbolo, Estado destino) {
        Vector tr = new Vector();
        
        // Si el indice del estado es mayor que el tamaño de delta, aumentamos
        // su tamaño.
        if (estado>=delta.size()) {
            delta.setSize(estado+1);
            // Reservamos la memoria
            delta.setElementAt(new Vector(),estado);
        }
        // si no hay que aumentar el tamaño, pero la posicion apunta a null,
        // reservamos la memoria para el nuevo elemento.
        if (delta.elementAt(estado)==null) delta.setElementAt(new Vector(),estado);
        tr = (Vector)delta.elementAt(estado);
        
        // Lo mismo que para delta.
        Vector tmpTR = new Vector();
        if (simbolo>=tr.size()) {
            tr.setSize(simbolo+1);
            tr.setElementAt(new Vector(),simbolo);
            tmpTR = (Vector)tr.elementAt(simbolo);
            if (!tmpTR.contains(destino))
                tmpTR.addElement(new Estado(destino));
            tr.setElementAt(tmpTR,simbolo);
        }
        else {
            if (tr.elementAt(simbolo)==null) tr.setElementAt(new Vector(),simbolo);
            tmpTR = (Vector)tr.elementAt(simbolo);
            if (!tmpTR.contains(destino)) 
                tmpTR.addElement(new Estado(destino));
            tr.setElementAt(tmpTR,simbolo);
        }
        // Delta es un vector de vectores de vectores de Estados ( flipa :) ).
        delta.setElementAt(tr,estado);
    }
    
    /**
     * Funcion que devuelve todas las transiciones de un estado dado.
     * @param estado Indice el estado del que queremos la matriz de transiciones
     *@return Un vector que contiene las transiciones para ese estado
     */
    public Vector getVectorTransicion(int estado) throws Exception {
        if (estado>delta.size()) throw new Exception("No existen transiciones para ese estado");
        else return (Vector)delta.elementAt(estado);
    }
    
    /**
     * Dado un estado y un simbolo, nos dice a donde vamos.
     *@param estado Estado para el que queremos saber la transicion
     *@param simbolo Simbolo con el que buscaremos la transicion
     *@return Un vector que contiene todas transciones de ese estado con ese simbolo
     */
    public Vector getTransicion(int estado, int simbolo) throws Exception {
        Vector n = new Vector();
        if (estado>=delta.size()||delta.isEmpty()) throw new Exception("Ese estado no tiene transiciones");
        else {
            n = (Vector)delta.elementAt(estado);
            if (simbolo>=n.size()||n.isEmpty()||n.elementAt(simbolo)==null) throw new Exception("No hay transición para ese símbolo");
            else return (Vector)n.elementAt(simbolo);
        }
    }
    
    /**
     *  Devuelve un estado. Quizir, le damos un estado y una cadena del alfabeto
     *   (por ejemplo: desde % (lambda) con la cadena 101) y nos tiene que devolver
     *   el estado al que vamos. Ojo, un UNICO estado. Si el automata no es
     *   deterministico nos devuelve el primer estado del vector.
     *@param estado Indice del estado del que partiremos para calcular delta estrella
     *@param cadena Cadena de transiciones a calcular
     *@return Estado al que llegamos desde el estado dado y para esa cadena
     */
    public Estado getTransicionEstrella(int estado, String cadena) throws Exception {
        Estado etemp = new Estado((Estado)vEstados.elementAt(estado));
        Vector aux = new Vector();
        String simbActual,cadActual;
        cadActual = cadena;
        for (int i=0; i<cadena.length(); i++) {
            simbActual = cadActual.substring(0,1);
            cadActual = cadActual.substring(1);
            try {
                aux = (Vector)getTransicion(buscarEstado(etemp),simbolos.indexOf(simbActual));
                etemp = (Estado)aux.elementAt(0);
            }
            catch (Exception err) {
                throw new Exception("No llega a ningun estado valido: "+err);
            }
        }
        return etemp;
    }
    
    /**
     * Modifica el tipo de automata
     *@param t Nuevo tipo de automata
     *@return No devuelve nada
     */
    public void putTipoAutomata(String t) {
        tipo = t;
    }
    
    /** 
     * Devuelve el tipo de automata.
     *@return El tipo de automata. Puede ser: INICIAL, INICIAL/FINAL, INTERMEDIO o FINAL
     */
    public String getTipoAutomata() {
        return tipo;
    }
    
    /**
     *  FUncion que une dos estados
     *@param primero Primer indice de estado a unir
     *@param segundo Segundo indice de estado a unir
     *@return No devuelve nada
     */
    public void uneEstados(int primero, int segundo) {
        Estado tmp1,tmp2 = new Estado();
        String tipo;
        tmp1 = this.obtenerEstado(primero);
        tmp2 = this.obtenerEstado(segundo);
        for (int i=0; i<tmp2.getNumEstados(); i++) {
            // Hay que mirar que estado es mas importante (tipo). El tipo
            //  resultante de la union es el mas importante (es decir, si se une
            //  un INTERMEDIO y un FINAL, el resultado es FINAL).
            if (tmp1.getTipoEstado().equals("INTERMEDIO")) tipo = tmp2.getTipoEstado();
            else if (tmp2.getTipoEstado().equals("INTERMEDIO")) tipo = tmp1.getTipoEstado();
            else if (((tmp1.getTipoEstado().equals("INICIAL")) && (tmp2.getTipoEstado().equals("FINAL"))) || ((tmp2.getTipoEstado().equals("INICIAL")) && (tmp1.getTipoEstado().equals("FINAL"))))
                tipo = "INICIAL/FINAL";
            else if (tmp1.getTipoEstado().equals(tmp2.getTipoEstado())) tipo = tmp1.getTipoEstado();
            else tipo = tmp1.getTipoEstado();
            tmp1.addEstado(tmp2.getEstado(i),tipo);
        }
        vEstados.setElementAt((Estado)tmp1,primero);
        this.delEstado((Estado)tmp2);
        /* 
         * IMPORTANTE
         * IMPORTANTE: Une los estados, pero las transiciones hay que ponerlas
         * IMPORTANTE:   usando la funcion addTransicion(...) 
         * IMPORTANTE
        */
    }
    
    /**
     * Guardamos el autómata en un fichero de texto. Solo necesita un parametro,
     *  indicando si queremos guardar el automata en modo compacto o no.
     * Produce un fichero de texto que contiene el automata.
     *@param compacto Booleano indicando si lo queremos compacto (true) o no (false)
     *@param nombreFichero Nombre del fichero donde se guardará el automata
     *@return No devuelve nada
    */
    public void guardarAutomata(boolean compacto, String nombreFichero) {
        try {
            String tF = nombreFichero;
            //if (compacto==false) tF = "automata.txt";
            //else tF = "automataCompacto.txt";
            FileWriter fw = new FileWriter(tF);
            BufferedWriter bw = new BufferedWriter(fw);
            PrintWriter salida = new PrintWriter(bw);
            int i,j,k;
            
            // Sacamos el conjunto de estados
            salida.println("Estados: ");salida.println();
            Estado t = new Estado();
            for (i=0; i<vEstados.size(); i++) {
                t = (Estado)vEstados.elementAt(i);
                // Si es en modo compacto ponemos el indice del estado
                if (compacto) salida.print(i+". ");
                salida.print("["+t.getTipoEstado()+"] ");
                if (t.getNumEstados()==1) {
                    salida.println(t.getNombreEstado().elementAt(0));
                }
                else {
                    for (j=0; j<t.getNumEstados()-1; j++) {
                        salida.print(t.getNombreEstado().elementAt(j)+",");
                    }
                    salida.println(t.getNombreEstado().elementAt(j));
                }
            }
            salida.println();

            // El alfabeto del automata
            salida.println("Alfabeto: ");salida.println();
            for (i=0; i<simbolos.size(); i++)
                salida.println(simbolos.elementAt(i).toString());
            salida.println();
            
            // Matriz de transiciones
            salida.println("Matriz de transiciones: ");salida.println();
            salida.print("Estado ");
            for (i=0; i<simbolos.size(); i++) salida.print(simbolos.elementAt(i)+" ");
            salida.println();
            
            Estado tmp = new Estado();
            Vector vtmp = new Vector();
            for (i=0; i<vEstados.size(); i++) {
                t = (Estado)vEstados.elementAt(i);
                if (compacto) {
                    salida.print("q"+this.buscarEstado(t));
                }
                else {
                    salida.print("{"+t.getEstado(0));
                    for (k=1; k<t.getNumEstados(); k++) {
                        salida.print(",");
                        salida.print(t.getEstado(k));
                    }
                    salida.print("}");
                }
                salida.print(" ");
                
                //Mostramos las transiciones para ese estado
                for (j=0; j<simbolos.size(); j++) {
                    try {
                        vtmp = (Vector)this.getTransicion(i,j);
                        for (int z=0; z<vtmp.size(); z++) {
                            tmp = (Estado)vtmp.elementAt(z);
                            if (compacto) salida.print("q"+this.buscarEstado(tmp));
                            else {
                                tmp = (Estado)vtmp.elementAt(z);
                                salida.print("{"+tmp.getEstado(0));
                                for (k=1; k<tmp.getNumEstados(); k++)
                                    salida.print(","+tmp.getEstado(k));
                                salida.print("}");
                            }
                            if ((vtmp.size()>1)&&(z<vtmp.size()-1)) salida.print(",");
                        }
                        salida.print(" ");
                    }
                    catch (Exception error) {
                        salida.print("- ");
                    }
                }
                salida.println();
            }
            
            //Cerramos el Fichero
            salida.close();
        }
        catch (Exception err) {
            JOptionPane.showMessageDialog(null,"Error al escribir en el fichero","Guardar autómata",JOptionPane.ERROR_MESSAGE);
        }
    }

}
