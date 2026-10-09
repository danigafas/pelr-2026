/*
 * Estado.java
 *
 * Created on 15 de diciembre de 2006, 17:25
 *
 * Daniel Moral García
 *
 */

package estdatos;
import java.util.Vector;
import java.lang.String;
import java.io.Serializable;

public class Estado implements Serializable {

    // Vector con los nombres de los estados.
    private Vector nombreEstado;
    
    // Tipo de estado. Puede ser INICIAL, FINAL, INICIAL/FINAL o INTERMEDIO
    private String tipoEstado;
    
    // Alfabeto de salida para el estado. ¿?¿?
    private Vector alfabetoSalida;
    
    /**
     *  Contructor por defecto de un estado. No necesita nada y produce una
     *   nueva instancia para este tipo.
    */
    public Estado() {
        nombreEstado = new Vector();
        // Por defecto se pone tipo intermedio
        tipoEstado = "INTERMEDIO";
        // En principio vacio. Solo se necesita para las maquinas de Moore
        //alfabetoSalida = new Vector();
    }
    
    /**
     *  Contructor para la clase estado al que se le pasa un estado y el tipo
     *   de estado que es.
    */
    public Estado(Vector nEstado, String te) {
        nombreEstado = (Vector)nEstado.clone();
        tipoEstado = te;
        //alfabetoSalida = new Vector();
    }
        
    /**
     *  Constructor para la clase estado al que se le pasa un nombre, un tipo
     *   y un alfabeto de salida.
    */
    public Estado(Vector nEstado, String te, Vector aSalida) {
        nombreEstado = (Vector)nEstado.clone();
        tipoEstado = te;
        //alfabetoSalida = (Vector)aSalida.clone();
    }
    
    // Constructor que necesita un String, que sera el nombre del estado
    public Estado(String e) {
        nombreEstado = new Vector();
        nombreEstado.addElement(e);
    }
    
    // Igual que el anterior pero indicandole el tipo del estado.
    public Estado(String e, String t) {
        nombreEstado = new Vector();
        nombreEstado.addElement(e);
        tipoEstado = t;
    }
    
    /**
     *  Constructor copia de la clase estado.
    */
    public Estado(Estado e) {
        nombreEstado = (Vector)e.nombreEstado.clone();
        tipoEstado = e.tipoEstado;
        //alfabetoSalida = (Vector)e.alfabetoSalida.clone();
    }
    
    /**
     * Funcion que devuelve los estados de un estado.
     *@return Un vector que contiene todos los estados de un estado
     */
    public Vector getNombreEstado() {
        return nombreEstado;
    }
    
    /**
     * Devuelve un String con el tipo de estado.
     *@return Un string con el tipo de estado.
     */
    public String getTipoEstado() {
        return tipoEstado;
    }
    
    /**
     * Devuelve un String que contiene el alfabeto de salida.
     * @return Un vector que contiene el alfabeto de salida
     */
    public Vector getAlfabetoS() {
        return alfabetoSalida;
    }
    
    /** 
     *  Funcion para modificar el nombre del estado. Necesita un nombre de 
     *   estado y el indice para ese estado. No devuelve nada.
     *@param nEstado
     *@return No devuelve nada
    */
    public void putNombreEstado(Vector nEstado) {
        nombreEstado = (Vector)nEstado.clone();
    }
    
    /**
     * Modifica el tipo de estado. Necesita un String que contenga el tipo.
     *@param te
     *@return No devuelve nada
     */
    public void putTipoEstado(String te) {
        tipoEstado = te;
    }
    
    /**
     * Modifica el alfabeto de salida. Necesita un string.
     *@param as
     *@return No devuelve nada
     */
    public void putAlfabetoS(Vector as) {
        alfabetoSalida = (Vector)as.clone();
    }
    
    /**
     * Compara dos estados. devuelve cierto si son iguales y falso en caso
     *   contrario.
     *@param estado
     *@return Cierto si los estados son iguales. Falso en caso contrario.
    */
    public boolean comparaEstado(Estado estado) {
        if (estado.getNumEstados() == nombreEstado.size())
            for (int i=0; i<estado.getNumEstados(); i++) {
                if (!estado.getEstado(i).equals(nombreEstado.elementAt(i).toString())) return false;
            }
        else return false;
        return true;
    }
    
    /**
     * Devuelve el numero de elementos del estado
     *@return El numero de estados de dicho estado
     */
    public int obtenerNumeroEstados() {
        return nombreEstado.size();
    }
    
    /**
     * Añade un nuevo estado a la coleccion.
     *@param e Nombre del estado
     *@param te Tipo del estado
     *@return No devuelve nada
     */
    public void addEstado(String e, String te) {
        nombreEstado.addElement(e);
        tipoEstado = te;
    }
    
    /**
     * Elimina un estado de la coleccion.
     *@param e
     *@return No devuelve nada
     */
    public void delEstado(String e) {
        nombreEstado.removeElement(e);
    }
    
    /**
     * Nos da el estado correspondiente al indice
     *@param indice
     *@return El nombre del estado que ocupa la posicion indicada
     */
    public String getEstado(int indice) {
        return nombreEstado.elementAt(indice).toString();
    }
    
    /**
     * Nos devuelve el numero total de estados que tiene ese estado (valga
     *   la redundancia)
     *@return El numero de estados que contiene el estado
     */
    public int getNumEstados() {
        return nombreEstado.size();
    }
    
    /**
     *  @param e
     *  @return La posicion del estado dentro del estado.
     */
    public int getIndiceEstado(String e) {
        return nombreEstado.indexOf(e);
    }
    
}
