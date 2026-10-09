/*
 * Main.java
 *
 * Created on 15 de diciembre de 2006, 13:28
 *
 */

package pelr;

import Interfaz.JFramePrincipal;

/**
 *
 * @author Daniel Moral García
 */
public class Main {
    
    /** Creates a new instance of Main */
    public Main() {

    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {   
        JFramePrincipal pInicial = new JFramePrincipal();
        pInicial.setEnabled(true);
        pInicial.setVisible(true);
    }
   
}
