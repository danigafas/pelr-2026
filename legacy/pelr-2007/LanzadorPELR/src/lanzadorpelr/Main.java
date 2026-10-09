/*
 * Main.java
 *
 * Created on 25 de abril de 2007, 17:25
 *
 */

package lanzadorpelr;

import java.awt.Color;

/**
 *
 * @autor Daniel Moral García
 */
public class Main {
    
    /** Creates a new instance of Main */
    public Main() {
    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        JFramePrincipal l = new JFramePrincipal();
        l.setExtendedState(l.MAXIMIZED_BOTH);
        l.setEnabled(true);
        l.setVisible(true);
    }
    
}
