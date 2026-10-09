/*
 * AutomataOutput.java
 *
 * Created on 31 de marzo de 2007, 11:06
 *
 */

package estdatos;
import java.io.*;

/**
 *
 * @author Daniel Moral García
 */
public class AutomataOutput {
    private FileOutputStream file;
    private ObjectOutputStream output;
    
    /**
     * Para abrir el fichero
     *@return No devuelve nada
     */
    public void abrir() throws IOException {
        file = new FileOutputStream("aut.plr");
        output = new ObjectOutputStream(file);
    }
    
    /**
     * Para cerrar el fichero
     *@return No devuelve nada
     */
    public void cerrar() throws IOException {
        if (output!=null) output.close();
    }
    
    /** 
     * Para escribir en el fichero
     *@param a
     *@return No devuelve nada
     */
    public void escribir(Automata a) throws IOException {
        if (output!=null) output.writeObject(a);
    }    
}
