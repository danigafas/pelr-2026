/*
 * EstadoOutput.java
 *
 * Created on 31 de marzo de 2007, 10:51
 */

package estdatos;
import java.io.*;

/**
 *
 * @author Daniel Moral García
 */
  
public class EstadoOutput {
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
     *@param e
     *@return No devuelve nada
     */
    public void escribir(Estado e) throws IOException {
        if (output!=null) output.writeObject(e);
    }
}