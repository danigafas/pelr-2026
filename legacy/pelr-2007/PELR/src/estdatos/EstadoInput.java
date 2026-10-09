/*
 * EstadoInput.java
 *
 * Created on 31 de marzo de 2007, 10:59
 */

package estdatos;
import java.io.*;

/**
 *
 * @author Daniel Moral García
 */
public class EstadoInput {
    private FileInputStream file;
    private ObjectInputStream input;
    
    /**
     *@return No devuelve nada
     */
    public void abrir() throws IOException {
        file = new FileInputStream("aut.plr");
        input = new ObjectInputStream(file);
    }
    
    /**
     *@return No devuelve nada
     */
    public void cerrar() throws IOException {
        if (input!=null) input.close();
    }
    
    /**
     *@return Un estado leido de fichero
     */
    public Estado leer() throws IOException, ClassNotFoundException {
        Estado e = null;
        
        if (input!=null) {
            try {
                e = (Estado) input.readObject();
            }
            catch (EOFException eof) { 
                // Fin del fichero 
            }
        }
        return e;
    }
}
