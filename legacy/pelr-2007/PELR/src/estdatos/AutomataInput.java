/*
 * AutomataInput.java
 *
 * Created on 31 de marzo de 2007, 11:08
 *
 */

package estdatos;
import java.io.*;

/**
 *
 * @author Daniel Moral García
 */
public class AutomataInput {
    private FileInputStream file;
    private ObjectInputStream input;
    
    /**
     * Funcion que abre el fichero
     *@return No devuelve nada
     */
    public void abrir() throws IOException {
        file = new FileInputStream("aut.plr");
        input = new ObjectInputStream(file);
    }
    
    /**
     *  Funcion que cierra el fichero
     *@return No devuelve nada
     */
    public void cerrar() throws IOException {
        if (input!=null) input.close();
    }
    
    /**
     *  Funcion que lee un automata
     *@return Devuelve un automata leido de fichero
     */
    public Automata leer() throws IOException, ClassNotFoundException {
        Automata a = null;
        
        if (input!=null) {
            try {
                a = (Automata) input.readObject();
            }
            catch (EOFException eof) { 
                // Fin del fichero 
            }
        }
        return a;
    } 
}
