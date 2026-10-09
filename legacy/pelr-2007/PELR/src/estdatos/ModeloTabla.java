/*
 * ModeloTabla.java
 *
 * Created on 27 de abril de 2007, 9:07
 *
 */

package estdatos;
import java.util.Vector;
import javax.swing.event.TableModelListener;
import javax.swing.table.TableModel;

/**
 *
 * @author Daniel Moral García
 */
public class ModeloTabla implements TableModel {
    String[][] data;
    String[] nombresC;
    
    /** Creates a new instance of miTabla */
    public ModeloTabla() {
        
    }
    
    public ModeloTabla(int filas, int columnas) {
        nombresC = new String[columnas];
        data = new String[filas][columnas];
    }
    
    /**
     * Pone nombre a una columna
     * @param columna Indice de la columna
     * @param aValue Valor de esa columna (nombre)
     * @return No devuelve nada
     */
    public void setNombreColumna(int columna, String aValue) {
        nombresC[columna] = aValue;
    }
    
    /**
     * Funcion que devuelve el nombre de una columna
     *@param columna
     *@return Un string que contiene el nombre de la columna
     */
    public String getNombreColumna(int columna) {
        return nombresC[columna];
    }
    
    /**
     *@return Devuelve el numero de filas
     */
    public int getRowCount() {
        return data.length;
    }
    
    /**
     *@return Devuelve el numero de columnas
     */
    public int getColumnCount() {
        return data[0].length;
    }
    
    /**
     *@param columnIndex
     *@return Devuelve la clase a la que pertenece la columna
     */
    public Class getColumnClass(int columnIndex) {
        return String.class;
    }
    
    /**
     *@param rowIndex Indice de la fila
     *@param columnIndex Indice de la columna
     *@return Devuelve falso porque las celdas no son editables
     */
    public boolean isCellEditable(int rowIndex, int columnIndex) {
        return false;
    }
    
    /**
     *@param rowIndex Indice de la fila
     *@param columnIndex Indice de la columna
     *@return Devuelve el valor de la celda
     */
    public Object getValueAt(int rowIndex, int columnIndex) {
        return data[rowIndex][columnIndex];
    }
    
    /**
     *@param aValue Valor a introducir
     *@param rowIndex Indice de la fila
     *@param columnIndex Indice de la columna
     *@return No devuelve nada
     */
    public void setValueAt(Object aValue, int rowIndex, int columnIndex) {
        data[rowIndex][columnIndex] = aValue.toString();
    }
    
    public void addTableModelListener(TableModelListener l) {

    }
    
    public void removeTableModelListener(TableModelListener l) {

    }

    /**
     *@param columnIndex Indice de la columna
     *@return Devuelve el nombre de la columna
     */
    public String getColumnName(int columnIndex) {
        return nombresC[columnIndex];
    }
    
}
